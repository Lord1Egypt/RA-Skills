#!/usr/bin/env python3
"""tracing.py — QCM MCP OpenTelemetry 分布式追踪

功能：
  - TracerProvider（OpenTelemetry SDK · Console 导出）
  - span 记录：工具调用（name/arguments/duration/status）
  - 上下文传播（trace_id/span_id）
  - 环境变量：QCM_TRACING=1 启用（默认开）
  - QCM_TRACE_EXPORTER=console|otlp（默认 console）

用法：
  from tracing import get_tracer, start_tool_span, tracing_enabled

  # 在工具调用处
  span = start_tool_span("qcm_research", {"query": "..."})
  try:
      result = handler(...)
      span.end()
      return result
  except Exception as e:
      span.record_exception(e)
      span.end()
      raise
"""
import os
import sys
import time
import json
import uuid
import pathlib
from typing import Dict, Optional, Any

_dr = None


def _dep_reg():
    global _dr
    if _dr is None:
        _core = str(pathlib.Path(__file__).resolve().parents[2] / "core")
        if _core not in sys.path:
            sys.path.insert(0, _core)
        import dep_registry as _mod
        _dr = _mod
    return _dr

# ============ 轻量 span 实现（不依赖 OTel SDK · 格式兼容）============
class Span:
    """最小 span 实现（兼容 OpenTelemetry span 语义）"""

    def __init__(self, name: str, attributes: Optional[Dict] = None,
                 parent_span_id: Optional[str] = None):
        self.name = name
        self.attributes = attributes or {}
        self.span_id = uuid.uuid4().hex[:16]
        self.trace_id = uuid.uuid4().hex[:32]
        self.parent_span_id = parent_span_id
        self.start_time_ns = time.time_ns()
        self.end_time_ns: Optional[int] = None
        self.status = "OK"
        self.events: list = []

    def set_attribute(self, key: str, value: Any):
        self.attributes[key] = value

    def record_exception(self, exc: Exception):
        self.events.append({
            "name": "exception",
            "attributes": {"exception.type": type(exc).__name__,
                           "exception.message": str(exc)[:500]},
        })
        self.status = "ERROR"

    def end(self):
        if self.end_time_ns is None:
            self.end_time_ns = time.time_ns()

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "trace_id": self.trace_id,
            "span_id": self.span_id,
            "parent_span_id": self.parent_span_id,
            "status": self.status,
            "attributes": self.attributes,
            "events": self.events,
            "duration_ms": round((self.end_time_ns - self.start_time_ns) / 1e6, 2)
                if self.end_time_ns else None,
        }


# ============ 追踪器（尝试 OTel SDK · fallback 轻量）============
# 延迟初始化（首次使用时根据 env 构建 provider · 避免 OTel Once 单例冲突）
_OTEL_TRACER = None
OTEL_AVAILABLE = False
OTLP_AVAILABLE = False
OTLP_GRPC_AVAILABLE = False
_PROVIDER_INITIALIZED = False


def _init_provider() -> bool:
    """延迟初始化 OTel provider（根据 QCM_TRACE_EXPORTER 选择导出器）"""
    global _OTEL_TRACER, OTEL_AVAILABLE, OTLP_AVAILABLE, OTLP_GRPC_AVAILABLE
    global _PROVIDER_INITIALIZED
    if _PROVIDER_INITIALIZED:
        return OTEL_AVAILABLE
    _PROVIDER_INITIALIZED = True

    try:
        if not _dep_reg().is_available("opentelemetry"):
            raise ImportError("opentelemetry unavailable")
        from opentelemetry import trace as otel_trace
        from opentelemetry.sdk.trace import TracerProvider as OTelTracerProvider
        from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
        from opentelemetry.trace import Status, StatusCode

        provider = OTelTracerProvider()
        _exporter_name = os.environ.get("QCM_TRACE_EXPORTER", "console").lower()
        OTLP_AVAILABLE = False
        OTLP_GRPC_AVAILABLE = False
        if _exporter_name in ("otlp", "otlp-grpc", "otlp_grpc", "grpc"):
            try:
                if _exporter_name in ("otlp-grpc", "otlp_grpc", "grpc"):
                    # OTLP gRPC 导出（4317 端口 · Jaeger/Tempo/Collector）
                    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
                    _otlp_grpc_endpoint = os.environ.get("QCM_OTLP_GRPC_ENDPOINT",
                                                         "http://localhost:4317")
                    exporter = OTLPSpanExporter(endpoint=_otlp_grpc_endpoint)
                    OTLP_GRPC_AVAILABLE = True
                else:
                    # OTLP HTTP 导出（4318 端口）
                    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
                    _otlp_endpoint = os.environ.get("QCM_OTLP_ENDPOINT", "http://localhost:4318/v1/traces")
                    exporter = OTLPSpanExporter(endpoint=_otlp_endpoint)
                OTLP_AVAILABLE = True
            except ImportError:
                exporter = ConsoleSpanExporter()
        else:
            exporter = ConsoleSpanExporter()
        provider.add_span_processor(SimpleSpanProcessor(exporter))
        otel_trace.set_tracer_provider(provider)
        _OTEL_TRACER = otel_trace.get_tracer("qcm-mcp")
        OTEL_AVAILABLE = True
        return True
    except ImportError:
        OTEL_AVAILABLE = False
        return False


def _reset_provider():
    """测试用：重置 provider（下次 get_tracer 重新初始化）"""
    global _PROVIDER_INITIALIZED, _OTEL_TRACER, OTEL_AVAILABLE, OTLP_AVAILABLE, OTLP_GRPC_AVAILABLE
    _PROVIDER_INITIALIZED = False
    _OTEL_TRACER = None
    OTEL_AVAILABLE = False
    OTLP_AVAILABLE = False
    OTLP_GRPC_AVAILABLE = False


def tracing_enabled() -> bool:
    """追踪是否启用（QCM_TRACING=0 关闭）"""
    return os.environ.get("QCM_TRACING", "1") != "0"


def otlp_enabled() -> bool:
    """OTLP 导出是否启用（QCM_TRACE_EXPORTER=otlp|otlp-grpc）"""
    if not OTEL_AVAILABLE:
        _init_provider()
    name = os.environ.get("QCM_TRACE_EXPORTER", "").lower()
    return (OTLP_AVAILABLE and name in ("otlp", "otlp-grpc", "otlp_grpc", "grpc"))


def otlp_grpc_enabled() -> bool:
    """OTLP gRPC 导出是否启用（QCM_TRACE_EXPORTER=otlp-grpc）"""
    if not OTEL_AVAILABLE:
        _init_provider()
    name = os.environ.get("QCM_TRACE_EXPORTER", "").lower()
    return OTLP_GRPC_AVAILABLE and name in ("otlp-grpc", "otlp_grpc", "grpc")


def get_exporter_name() -> str:
    """当前导出器（console / otlp / otlp-grpc / none）"""
    if not OTEL_AVAILABLE:
        _init_provider()
    if not OTEL_AVAILABLE:
        return "none"
    return os.environ.get("QCM_TRACE_EXPORTER", "console").lower()


def get_tracer():
    """获取 tracer（OTel SDK 延迟初始化或轻量）"""
    if not OTEL_AVAILABLE:
        _init_provider()
    return _OTEL_TRACER


def start_tool_span(tool_name: str, arguments: Optional[Dict] = None) -> Optional[Span]:
    """启动工具调用 span

    Returns:
        OTel span（SDK 可用）或轻量 Span（fallback）
    """
    if not tracing_enabled():
        return None

    if not OTEL_AVAILABLE:
        _init_provider()
    if OTEL_AVAILABLE and _OTEL_TRACER:
        span = _OTEL_TRACER.start_span(
            f"tool:{tool_name}",
            attributes={"tool.name": tool_name,
                        "tool.arguments": json.dumps(arguments or {}, ensure_ascii=False)[:2000]},
        )
        # 包装为统一接口
        return _OTelSpanWrapper(span)
    return Span(f"tool:{tool_name}", {"tool.name": tool_name,
                                       "tool.arguments": json.dumps(arguments or {}, ensure_ascii=False)[:2000]})


class _OTelSpanWrapper:
    """OTel span 包装（统一 end/record_exception/to_dict 接口）"""

    def __init__(self, span):
        self._span = span
        self.start_time = time.time()
        self._status = "OK"
        self._events = []

    def set_attribute(self, key: str, value: Any):
        self._span.set_attribute(key, value)

    def record_exception(self, exc: Exception):
        self._status = "ERROR"
        self._events.append({
            "name": "exception",
            "attributes": {"exception.type": type(exc).__name__,
                           "exception.message": str(exc)[:500]},
        })
        self._span.record_exception(exc)
        try:
            self._span.set_status(Status(StatusCode.ERROR, str(exc)[:200]))
        except Exception:
            pass

    def end(self):
        try:
            self._span.set_attribute("duration_ms", round((time.time() - self.start_time) * 1000, 2))
        except Exception:
            pass
        self._span.end()

    def to_dict(self):
        try:
            attrs = dict(self._span.attributes) if hasattr(self._span, "attributes") else {}
        except Exception:
            attrs = {}
        try:
            ctx = self._span.get_span_context()
            trace_id = ctx.trace_id
            span_id = ctx.span_id
        except Exception:
            trace_id = span_id = "n/a"
        return {
            "name": getattr(self._span, "name", "otel-span"),
            "trace_id": trace_id,
            "span_id": span_id,
            "status": self._status,
            "attributes": attrs,
            "events": self._events,
            "duration_ms": round((time.time() - self.start_time) * 1000, 2),
        }


if __name__ == "__main__":
    # Demo
    span = start_tool_span("qcm_demo", {"query": "test"})
    if span:
        span.end()
        print(json.dumps(span.to_dict(), ensure_ascii=False, indent=2))
