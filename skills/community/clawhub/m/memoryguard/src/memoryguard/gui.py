"""原生桌面窗口 GUI（spec §6.1 第3步的桌面形态）。

依赖策略冲突解决（PREFERENCES §6）:
- spec §1.3/§10 要求零依赖、无供应链风险
- 用户需求要求原生桌面窗口，需 pywebview（第三方）
- 选择: pywebview 作为可选依赖 `memoryguard[gui]`，Core 本体保持零依赖。
  未安装时 open 自动降级到 localhost/HTML/文本。

能力降级链（spec §6.1）:
1. 桌面原生窗口 (pywebview 已装)  -- 本模块
2. localhost 浏览器窗口 (标准库 http.server)  -- 本模块
3. 静态 HTML 文件 (webbrowser.open file://)  -- cli.py
4. 结构化文本 + JSON 路径  -- cli.py
"""

from __future__ import annotations

import http.server
import socket
import threading
import webbrowser
from pathlib import Path


# ---------------------------------------------------------------------------
# 能力探测
# ---------------------------------------------------------------------------


def has_native_gui() -> bool:
    """探测 pywebview 是否可用（可选依赖）。"""
    try:
        import webview  # noqa: F401

        return True
    except ImportError:
        return False


# ---------------------------------------------------------------------------
# 1. 桌面原生窗口
# ---------------------------------------------------------------------------


def open_native_window(html_content: str, title: str = "MemoryGuard") -> int:
    """用 pywebview 弹原生桌面窗口加载 HTML 内容。

    返回退出码：0 成功，3 不可用需回退。
    阻塞调用：窗口关闭前不返回。
    """
    if not has_native_gui():
        return 3
    import webview

    # pywebview 加载 HTML 字符串，无需临时文件、无需 HTTP server
    webview.create_window(
        title=title,
        html=html_content,
        width=1200,
        height=800,
        min_size=(800, 600),
    )
    webview.start()
    return 0


# ---------------------------------------------------------------------------
# 2. localhost 浏览器窗口（降级路径）
# ---------------------------------------------------------------------------


def _find_free_port() -> int:
    """绑定 127.0.0.1 随机端口（spec §1.3 安全要求）。"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def open_localhost_window(html_content: str, *, auto_open: bool = True) -> tuple[int, str]:
    """启动临时本地 HTTP server，返回 (退出码, URL)。

    退出码：0 成功，3 无法绑定。
    阻塞调用：Ctrl+C 或 server.shutdown() 后返回。
    """
    port = _find_free_port()
    if port == 0:
        return 3, ""

    html_bytes = html_content.encode("utf-8")

    class _Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html_bytes)))
            self.end_headers()
            self.wfile.write(html_bytes)

        def log_message(self, *args):  # 静默
            pass

    server = http.server.HTTPServer(("127.0.0.1", port), _Handler)
    url = f"http://127.0.0.1:{port}/"
    if auto_open:
        try:
            webbrowser.open(url)
        except Exception:
            pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0, url


# ---------------------------------------------------------------------------
# 统一入口：按能力降级
# ---------------------------------------------------------------------------


def open_report_window(html_content: str, *, title: str = "MemoryGuard") -> int:
    """按 spec §6.1 降级链打开报告窗口。

    顺序: 桌面原生窗口 -> localhost 浏览器 -> (调用方继续降级到 HTML 文件)
    返回退出码：0 成功，3 需调用方继续降级。
    """
    if has_native_gui():
        return open_native_window(html_content, title=title)
    # 无 pywebview 时，由调用方决定是否走 localhost 还是直接 HTML 文件
    return 3


# ---------------------------------------------------------------------------
# 交互式治理面板（参考 merakagent Tab 布局，非平面报告）
# ---------------------------------------------------------------------------


class GovernanceApi:
    """pywebview JS API 类（v3 五入口架构，spec §7.2）。

    v3.1 新增：
    - pick_path：系统目录/文件选择器（替代 prompt）
    - discover_agents：AgentLocator 有限候选发现
    - get_selection_tree / commit_selection：分类勾选授权
    - neuron_decide：图上治理操作 → DecisionEvent → 新规范版本
    - 神经图投影 meta：Agent 实例 / Profile / 规范版本 / Release / 接管状态 / 覆盖状态 / 漂移
    """

    def __init__(self, workspace: str):
        self.workspace = workspace
        self._report = None
        self._window = None  # pywebview window 引用，由 open_interactive_window 注入

    def _set_window(self, window) -> None:
        """注入 pywebview window 实例（用于 create_file_dialog）。"""
        self._window = window

    # ------------------------------------------------------------------
    # 路径选择器（替代 prompt()）
    # ------------------------------------------------------------------

    def pick_path(self, for_files: bool = False) -> dict:
        """v3.1 §4.3 系统目录/文件选择器。

        for_files=False：选目录（默认，用于添加来源）
        for_files=True：选文件（用于导入离线导出包）

        返回 {path, is_directory} 或 {error: 'cancelled'}。
        """
        if self._window is None:
            # 无 pywebview window 时回退到 prompt
            path = input("输入路径：" if not for_files else "输入文件路径：")
            if not path:
                return {"error": "cancelled"}
            from pathlib import Path
            p = Path(path)
            return {"path": str(p.resolve()), "is_directory": p.is_dir()}
        try:
            import webview
            if for_files:
                file_types = (
                    "All files (*.*)|*.*|"
                    "Zip files (*.zip)|*.zip|"
                    "JSON files (*.json)|*.json|"
                    "JSONL files (*.jsonl)|*.jsonl"
                )
                result = self._window.create_file_dialog(
                    webview.OPEN_DIALOG, allow_multiple=False, file_types=file_types,
                )
            else:
                result = self._window.create_file_dialog(webview.FOLDER_DIALOG)
            if not result:
                return {"error": "cancelled"}
            path = result if isinstance(result, str) else result[0]
            from pathlib import Path
            p = Path(path)
            return {"path": str(p.resolve()), "is_directory": p.is_dir() if p.exists() else (not for_files)}
        except Exception as e:
            return {"error": f"dialog failed: {e}"}

    # ------------------------------------------------------------------
    # AgentLocator API（v3.1 §3.2）
    # ------------------------------------------------------------------

    def discover_agents(self) -> dict:
        """v3.1 §3.2 检测本机已安装的 Agent 实例。"""
        from .agent_locator import AgentLocator
        locator = AgentLocator(self.workspace)
        instances, ledgers = locator.detect_instances()
        # 持久化 discovery 结果
        if instances:
            locator.save_discovery(instances, ledgers)
        # 聚合发现账本
        agg_counts = {"found": 0, "missing": 0, "unsupported": 0,
                      "permission_denied": 0, "excluded_by_user": 0,
                      "not_applicable": 0, "unaccounted_count": 0}
        for ledger in ledgers.values():
            cnt = ledger.counts()
            for k in agg_counts:
                agg_counts[k] += cnt.get(k, 0)
        return {
            "instances": [i.to_dict() for i in instances],
            "discovery_ledger": agg_counts,
            "platform": locator.context.platform,
            "host_id": locator.context.host_id,
        }

    def get_selection_tree(self, instance_id: str) -> dict:
        """v3.1 §4.3 返回分类勾选树。"""
        from .agent_locator import AgentLocator
        locator = AgentLocator(self.workspace)
        return locator.get_selection_tree(instance_id)

    def commit_selection(self, instance_id: str, selected: list, confirmed: bool = False) -> dict:
        """v3.1 §4.3 写入 SelectionManifest + 授权 SourceRoot。

        selected 是 [{category, path}, ...] 列表。
        """
        if not confirmed:
            return {"error": "需要确认才能提交勾选"}
        from pathlib import Path
        from .schema_v3 import (
            SourceRoot, SourceRootType, stable_hash, _now_iso,
            SelectionManifest, SelectionEntry,
            SourceCategory, IngestionPolicy, Ownership, TargetRole,
        )
        from .source_registry import SourceRegistry
        import json

        # 加载 instance 信息以获取 profile_id
        from .agent_locator import AgentLocator
        locator = AgentLocator(self.workspace)
        tree = locator.get_selection_tree(instance_id)
        if "error" in tree:
            return tree
        # path → surface_id / ingestion_policy / etc 映射
        path_to_surface: dict[str, dict] = {}
        for cat in tree.get("categories", []):
            for f in cat.get("files", []):
                path_to_surface[f["path"]] = {
                    "surface_id": f["surface_id"],
                    "category": cat["category"],
                    "ingestion_policy": f["ingestion_policy"],
                    "ownership": f["ownership"],
                    "target_role": f["target_role"],
                }

        # 写入 SelectionManifest
        sel_dir = Path(self.workspace) / ".memoryguard" / "selections"
        sel_dir.mkdir(parents=True, exist_ok=True)
        selection_id = stable_hash("sel", instance_id, _now_iso())
        entries: list[SelectionEntry] = []
        for item in selected:
            path = item.get("path", "")
            cat_str = item.get("category", "unknown")
            surf = path_to_surface.get(path, {})
            try:
                cat_enum = SourceCategory(cat_str)
            except ValueError:
                cat_enum = SourceCategory.UNKNOWN
            try:
                ing = IngestionPolicy(surf.get("ingestion_policy", "extract_candidates"))
            except ValueError:
                ing = IngestionPolicy.EXTRACT_CANDIDATES
            try:
                own = Ownership(surf.get("ownership", "external_read_only"))
            except ValueError:
                own = Ownership.EXTERNAL_READ_ONLY
            try:
                tr = TargetRole(surf.get("target_role", "none"))
            except ValueError:
                tr = TargetRole.NONE
            entries.append(SelectionEntry(
                surface_id=surf.get("surface_id", ""),
                resolved_path=path, category=cat_enum,
                ingestion_policy=ing, ownership=own, target_role=tr,
                selected=True,
            ))
        manifest = SelectionManifest(
            selection_id=selection_id, instance_id=instance_id,
            profile_id=tree.get("profile_id", ""),
            created_at=_now_iso(), entries=entries,
            authorization_summary={
                "selected_count": len(entries),
                "native_memory_count": sum(1 for e in entries if e.category == SourceCategory.NATIVE_MEMORY),
                "control_surface_count": sum(1 for e in entries if e.category == SourceCategory.CONTROL_SURFACE),
            },
        )
        (sel_dir / f"{selection_id}.json").write_text(
            json.dumps(manifest.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        # 授权 SourceRoot（每个 path 一个 SourceRoot）
        # v3.1 §4.3：root_id 一致性 —— SourceRegistry.add() 内部用
        # "src-" + stable_hash(str(p), type.value) 做去重，所以这里直接调用 add()，
        # 然后幂等地补充 v3.1 §4.2 字段。已存在且已设置 agent_instance_id 的跳过。
        reg = SourceRegistry(self.workspace)
        added_count = 0
        updated_count = 0
        for entry in entries:
            p = Path(entry.resolved_path)
            if not p.exists():
                continue
            root_type = SourceRootType.SELECTED_DIRECTORY if p.is_dir() else SourceRootType.SELECTED_FILE
            try:
                root = reg.add(entry.resolved_path, root_type,
                               display_name=f"{tree.get('product', 'agent')}/{entry.surface_id}")
            except (ValueError, OSError):
                continue
            # 幂等补充 v3.1 §4.2 新字段
            if root.agent_instance_id and root.agent_instance_id != instance_id:
                continue  # 已被其他 instance 占用，不覆盖
            if not root.agent_instance_id:
                root.agent_instance_id = instance_id
                root.surface_id = entry.surface_id
                root.source_category = entry.category.value
                root.ingestion_policy = entry.ingestion_policy.value
                root.ownership = entry.ownership.value
                root.target_role = entry.target_role.value
                added_count += 1
            else:
                updated_count += 1
        reg._save()
        return {
            "selection_id": selection_id,
            "added_source_count": added_count,
            "updated_source_count": updated_count,
            "total_selected": len(entries),
        }

    # ------------------------------------------------------------------
    # 图上治理操作（v3.1 §6.2）
    # ------------------------------------------------------------------

    def neuron_decide(self, node_id: str, action: str,
                      reason: str = "", confirmed: bool = False) -> dict:
        """v3.1 §6.2 图上操作 → 追加 DecisionEvent → 新规范版本。

        action ∈ {accept, exclude, quarantine, supersede, merge, rescope, plan}
        """
        if not confirmed:
            return {"error": "需要确认才能执行治理操作"}
        from .managed_store import ManagedStore, find_record_by_node_id
        # 找到记录对应的 agent_instance_id
        vid, record = find_record_by_node_id(self.workspace, node_id)
        if record is None:
            return {"error": f"node not found in any managed store: {node_id}"}
        # 找 agent_instance_id
        from pathlib import Path
        ws = Path(self.workspace).resolve()
        mm_root = ws / ".memoryguard" / "managed-memory"
        agent_instance_id = None
        for inst_dir in mm_root.iterdir():
            if not inst_dir.is_dir():
                continue
            store = ManagedStore(ws, inst_dir.name)
            recs = store.list_records()
            if any(r.memory_id == record.memory_id for r in recs):
                agent_instance_id = inst_dir.name
                break
        if agent_instance_id is None:
            return {"error": "agent instance not found for record"}
        store = ManagedStore(ws, agent_instance_id)
        new_version = store.apply_decision(
            action=action, target_ids=[record.memory_id],
            reason=reason, actor="user",
        )
        return {
            "memory_version": new_version.version_id,
            "action": action,
            "target_id": record.memory_id,
            "decision_count": new_version.decision_count,
        }

    # ------------------------------------------------------------------
    # ProjectionApi（spec §7.3）：神经图纯投影
    # ------------------------------------------------------------------

    def get_neuron_graph(self) -> dict:
        """纯读取神经图投影。未构建时返回 {empty: true, reason: 'not_built'}。"""
        from .projection import ProjectionBuilder
        pb = ProjectionBuilder(self.workspace)
        return pb.get_or_empty()

    def build_projection(self, confirmed: bool = False) -> dict:
        """构建神经图投影（需用户确认）。

        v3.1 §6.3：构建时同步为每个 agent_instance 创建 ManagedStore initial
        version（若不存在），并聚合 7 项 meta 信息注入投影。
        """
        if not confirmed:
            return {"error": "需要确认才能构建投影"}
        from .memory_ir import MemoryNormalizer
        from .projection import ProjectionBuilder
        from .source_registry import SourceRegistry, ScanBudget
        from .managed_store import ManagedStore
        from .agent_locator import AgentLocator, compute_takeover_state
        from .schema_v3 import TakeoverState
        from pathlib import Path

        reg = SourceRegistry(self.workspace)
        snap = reg.scan(ScanBudget())
        root_map = {r.root_id: r.path for r in reg.list_sources()}

        norm = MemoryNormalizer(self.workspace)
        ir = norm.load()
        if ir is None or ir.snapshot_id != snap.snapshot_id:
            ir = norm.normalize(snap, root_map=root_map)
            norm.save(ir)

        # 建立 source_object_id → source_root_id → agent_instance_id 映射
        obj_to_root = {obj.source_object_id: obj.source_root_id
                       for obj in snap.source_objects}
        root_to_instance = {r.root_id: r.agent_instance_id
                            for r in reg.list_sources() if r.agent_instance_id}

        # 按 agent_instance_id 分组 records
        instance_records: dict[str, list] = {}
        for rec in ir.records:
            for prov in rec.provenance:
                root_id = obj_to_root.get(prov.source_object_id, "")
                inst_id = root_to_instance.get(root_id, "")
                if inst_id:
                    instance_records.setdefault(inst_id, []).append(rec)
                    break

        # 为每个 agent_instance 创建/更新 ManagedStore initial version
        managed_meta: dict[str, dict] = {}
        for inst_id, recs in instance_records.items():
            store = ManagedStore(self.workspace, inst_id)
            if store.get_active_version_id() is None:
                store.create_initial_version(recs)
            active = store.get_active_version()
            managed_meta[inst_id] = {
                "version_id": active.version_id if active else "",
                "record_count": len(recs),
                "decision_count": active.decision_count if active else 0,
            }

        # 聚合 7 项状态 meta
        locator = AgentLocator(self.workspace)
        instances, ledgers = locator.detect_instances()
        cov_counts = snap.coverage.counts()
        cov_status = snap.coverage.status().value
        # 读取已发布的 release（若有）
        releases_list: list[dict] = []
        try:
            from .release_manager import ReleaseManager
            rm = ReleaseManager(self.workspace)
            releases_list = rm.list_releases()
        except Exception:
            pass

        agent_instances_meta = []
        for inst in instances:
            inst_ledger = ledgers.get(inst.instance_id)
            mm = managed_meta.get(inst.instance_id, {})
            has_managed = bool(mm)
            # 接管状态机
            takeover_state = compute_takeover_state(
                instance=inst,
                ledger=inst_ledger,
                selection_committed=has_managed,
                canonicalized=has_managed,
                release_planned=any(r.get("instance_id") == inst.instance_id
                                    for r in releases_list),
                published=any(r.get("instance_id") == inst.instance_id
                              and r.get("status") == "applied"
                              for r in releases_list),
                runtime_verified=False,
                drifted=False,
            )
            agent_instances_meta.append({
                "instance_id": inst.instance_id,
                "product": inst.product,
                "profile_id": inst.profile_id,
                "target_capability": inst.target_capability.value,
                "managed_version": mm.get("version_id", ""),
                "record_count": mm.get("record_count", 0),
                "decision_count": mm.get("decision_count", 0),
                "takeover_state": takeover_state.value,
            })

        meta = {
            "agent_instances": agent_instances_meta,
            "instance_count": len(agent_instances_meta),
            "coverage": cov_counts,
            "coverage_status": cov_status,
            "release_count": len(releases_list),
            "drifted": False,
        }

        pb = ProjectionBuilder(self.workspace)
        proj = pb.build(ir, meta=meta)
        pb.save(proj)
        return proj.to_dict()

    def delete_projection(self, confirmed: bool = False) -> dict:
        """删除神经图投影文件。投影可从 IR + DecisionLog 完整重建。"""
        if not confirmed:
            return {"error": "需要确认才能删除投影"}
        from .projection import ProjectionBuilder
        pb = ProjectionBuilder(self.workspace)
        pb.delete()
        return {"ok": True, "deleted": True}

    # ------------------------------------------------------------------
    # SourceApi（spec §7.2）
    # ------------------------------------------------------------------

    def list_sources(self) -> dict:
        from .source_registry import SourceRegistry
        reg = SourceRegistry(self.workspace)
        sources = [s.to_dict() for s in reg.list_sources()]
        return {"sources": sources, "total": len(sources)}

    # ------------------------------------------------------------------
    # DataApi（v3.2 §8.2）：Agent 卡片数据页
    # ------------------------------------------------------------------

    def list_agent_candidates(self, include_uninstalled: bool = False,
                              include_stale: bool = True,
                              include_unknown: bool = True) -> dict:
        """v3.2 扫描当前系统 HOME 下的所有 Agent 候选。

        返回候选列表，含 stale 状态、是否已标记卸载、是否有 Profile。
        """
        from .agent_locator import AgentLocator
        locator = AgentLocator(self.workspace)
        candidates = locator.discover_candidates(
            include_uninstalled=include_uninstalled,
            include_stale=include_stale,
            include_unknown=include_unknown,
        )
        return {
            "candidates": [c.to_dict() for c in candidates],
            "total": len(candidates),
        }

    def mark_agent_uninstalled(self, product: str, dir_path: str = "",
                               reason: str = "") -> dict:
        """标记 Agent 为已卸载，后续扫描跳过。"""
        from .agent_cleanup import AgentCleanup
        cleanup = AgentCleanup(self.workspace)
        return cleanup.mark_uninstalled(product, dir_path=dir_path, reason=reason)

    def unmark_agent_uninstalled(self, product: str) -> dict:
        """取消已卸载标记。"""
        from .agent_cleanup import AgentCleanup
        cleanup = AgentCleanup(self.workspace)
        return cleanup.unmark_uninstalled(product)

    def archive_agent_dir(self, product: str, dir_path: str,
                          reason: str = "") -> dict:
        """归档 Agent 目录到 .memoryguard/cleanup/archived-agents/。可恢复。"""
        from .agent_cleanup import AgentCleanup
        cleanup = AgentCleanup(self.workspace)
        return cleanup.archive_agent_dir(product, dir_path, reason=reason)

    def restore_archived_agent(self, archive_id: str) -> dict:
        """从归档恢复 Agent 目录。"""
        from .agent_cleanup import AgentCleanup
        cleanup = AgentCleanup(self.workspace)
        return cleanup.restore_archived(archive_id)

    def list_archived_agents(self) -> dict:
        """列出所有归档的 Agent。"""
        from .agent_cleanup import AgentCleanup
        cleanup = AgentCleanup(self.workspace)
        return {"archives": cleanup.list_archives(), "total": len(cleanup.list_archives())}

    def list_cleanup_history(self) -> dict:
        """读取清理操作历史。"""
        from .agent_cleanup import AgentCleanup
        cleanup = AgentCleanup(self.workspace)
        return {"history": cleanup.list_cleanup_history()}

    def list_agents(self) -> dict:
        """v3.2 数据页 Agent 卡片：返回已发现的 Agent 实例列表。

        每个卡片含：instance_id, product, profile_id, surfaces 摘要,
        已绑定 SourceRoot 数量, native_memory_mode 预期。
        """
        from .agent_locator import AgentLocator
        from .source_registry import SourceRegistry
        locator = AgentLocator(self.workspace)
        instances, _ledgers = locator.detect_instances()
        reg = SourceRegistry(self.workspace)
        # root_id -> agent_instance_id 映射，统计每个 agent 的 SourceRoot 数量
        agent_root_counts: dict[str, int] = {}
        for r in reg.list_sources():
            if r.agent_instance_id:
                agent_root_counts[r.agent_instance_id] = agent_root_counts.get(r.agent_instance_id, 0) + 1
        cards = []
        for inst in instances:
            found_count = sum(1 for s in inst.surfaces if s.get("status") == "found")
            cards.append({
                "instance_id": inst.instance_id,
                "product": inst.product,
                "profile_id": inst.profile_id,
                "target_capability": inst.target_capability.value,
                "surface_count": len(inst.surfaces),
                "found_surface_count": found_count,
                "bound_source_count": agent_root_counts.get(inst.instance_id, 0),
                "platform": inst.platform,
                "host_id": inst.host_id,
            })
        return {"agents": cards, "total": len(cards)}

    def get_agent_data(self, instance_id: str) -> dict:
        """v3.2 数据页：返回单个 Agent 的完整数据视图。

        按数据类别分组：native_memory / control_surface / skill_surface /
        conversation_history / project_document。
        """
        from .source_registry import SourceRegistry, ScanBudget
        reg = SourceRegistry(self.workspace)
        snap = reg.scan(ScanBudget())
        # 该 Agent 的 SourceRoot 列表
        agent_roots = [r for r in reg.list_sources() if r.agent_instance_id == instance_id]
        root_map = {r.root_id: r for r in agent_roots}
        # 按 source_category 分组
        categories: dict[str, list[dict]] = {}
        for obj in snap.source_objects:
            root = root_map.get(obj.source_root_id)
            if not root:
                continue
            cat = root.source_category or "unknown"
            categories.setdefault(cat, []).append({
                "root_id": obj.source_root_id,
                "root_path": root.path,
                "display_name": root.display_name,
                "relative_path": obj.relative_path,
                "media_type": obj.media_type,
                "content_hash": obj.content_hash,
                "read_status": obj.read_status,
                "captured_at": obj.captured_at,
            })
        # Agent 基本信息
        from .agent_locator import AgentLocator
        locator = AgentLocator(self.workspace)
        instances, _ = locator.detect_instances()
        inst = next((i for i in instances if i.instance_id == instance_id), None)
        agent_info = {
            "instance_id": instance_id,
            "product": inst.product if inst else "unknown",
            "profile_id": inst.profile_id if inst else "",
            "surfaces": inst.surfaces if inst else [],
        }
        return {
            "agent": agent_info,
            "categories": categories,
            "total_files": sum(len(files) for files in categories.values()),
            "category_count": len(categories),
        }

    def enter_multi_agent_mode(self) -> dict:
        """v3.2 进入多 Agent 共享 MCP 模式。"""
        return {"mode": "multi_agent_shared_mcp", "ok": True}

    def exit_multi_agent_mode(self) -> dict:
        """v3.2 退回单 Agent 模式。"""
        return {"mode": "single_agent", "ok": True}

    # ------------------------------------------------------------------
    # BindingApi（v3.2 §8.2）：AgentBinding 与共享组
    # ------------------------------------------------------------------

    def list_bindings(self, include_inactive: bool = True) -> dict:
        from .agent_binding import AgentBindingStore
        store = AgentBindingStore(self.workspace)
        bindings = store.list_bindings(include_inactive=include_inactive)
        return {"bindings": [b.to_dict() for b in bindings], "total": len(bindings)}

    def bind_agent(self, agent_instance_id: str, share_group_id: str,
                   mcp_server_name: str = "memoryguard",
                   native_memory_mode: str = "observed",
                   redirect_paths: list[str] | None = None) -> dict:
        from .agent_binding import AgentBindingStore
        store = AgentBindingStore(self.workspace)
        binding = store.bind_agent(
            agent_instance_id=agent_instance_id,
            share_group_id=share_group_id,
            mcp_server_name=mcp_server_name,
            native_memory_mode=native_memory_mode,
            redirect_paths=redirect_paths or [],
        )
        return {"ok": True, "binding": binding.to_dict()}

    def bind_agents_to_shared_group(self, agent_instance_ids: list[str],
                                    share_group_id: str = "",
                                    mcp_server_name: str = "memoryguard",
                                    native_memory_modes: dict[str, str] | None = None,
                                    redirect_paths: dict[str, list[str]] | None = None) -> dict:
        from .agent_binding import AgentBindingStore
        store = AgentBindingStore(self.workspace)
        return store.bind_agents_to_group(
            agent_instance_ids=agent_instance_ids,
            share_group_id=share_group_id,
            mcp_server_name=mcp_server_name,
            native_memory_modes=native_memory_modes or {},
            redirect_paths=redirect_paths or {},
        )

    def unbind_agent(self, binding_id: str) -> dict:
        from .agent_binding import AgentBindingStore
        store = AgentBindingStore(self.workspace)
        binding = store.unbind_agent(binding_id)
        if binding is None:
            return {"error": f"binding not found: {binding_id}"}
        return {"ok": True, "binding": binding.to_dict()}

    def check_binding_drift(self, binding_id: str) -> dict:
        from .agent_binding import AgentBindingStore
        store = AgentBindingStore(self.workspace)
        return store.check_drift(binding_id)

    def get_shared_group_preview(self, share_group_id: str) -> dict:
        from .agent_binding import AgentBindingStore
        store = AgentBindingStore(self.workspace)
        return store.shared_group_preview(share_group_id)

    # ------------------------------------------------------------------
    # ExternalMCPApi（v3.2 §7）：外部 MCP 检测/导入
    # ------------------------------------------------------------------

    def detect_external_mcp(self, server_id: str, descriptor: dict) -> dict:
        from .external_mcp_detector import ExternalMCPDetector
        detector = ExternalMCPDetector(self.workspace)
        return detector.detect_server(server_id, descriptor)

    def list_external_mcp_servers(self) -> dict:
        from .external_mcp_detector import ExternalMCPDetector
        detector = ExternalMCPDetector(self.workspace)
        servers = detector.list_servers()
        return {"servers": servers, "total": len(servers)}

    def preview_external_mcp_import(self, server_id: str, descriptor: dict | None = None) -> dict:
        from .external_mcp_detector import ExternalMCPDetector
        detector = ExternalMCPDetector(self.workspace)
        return detector.preview_import(server_id, descriptor)

    def import_external_mcp_entries(self, server_id: str, share_group_id: str,
                                    entries: list[dict],
                                    agent_instance_id: str = "external-mcp") -> dict:
        from .external_mcp_detector import ExternalMCPDetector
        detector = ExternalMCPDetector(self.workspace)
        return detector.import_entries(
            server_id=server_id,
            share_group_id=share_group_id,
            entries=entries,
            agent_instance_id=agent_instance_id,
        )

    # ------------------------------------------------------------------
    # MemoryApi（v3.2 §8.2）：记忆治理
    # ------------------------------------------------------------------

    def list_memory(self, status: str = "", kind: str = "",
                    share_group_id: str = "default") -> dict:
        """列出共享记忆，可按 status/kind 过滤。"""
        from .shared_memory_store import SharedMemoryStore
        store = SharedMemoryStore(self.workspace, share_group_id)
        records = store.list_records(status=status or None, kind=kind or None)
        return {
            "records": [r.to_dict() for r in records],
            "total": len(records),
            "status": store.status(),
        }

    def get_memory(self, memory_id: str, share_group_id: str = "default") -> dict:
        """读取单条记忆。"""
        from .shared_memory_store import SharedMemoryStore
        store = SharedMemoryStore(self.workspace, share_group_id)
        record = store.get_record(memory_id)
        if record is None:
            return {"error": f"memory not found: {memory_id}"}
        return record.to_dict()

    def search_memory(self, query: str, share_group_id: str = "default") -> dict:
        """搜索记忆。"""
        from .shared_memory_store import SharedMemoryStore
        store = SharedMemoryStore(self.workspace, share_group_id)
        records = store.list_records(status="active")
        query_lower = query.lower()
        matched = [r for r in records if query_lower in r.body.lower()]
        return {"records": [r.to_dict() for r in matched], "total": len(matched)}

    def edit_memory(self, memory_id: str, body: str,
                    share_group_id: str = "default") -> dict:
        """编辑记忆正文。"""
        from .shared_memory_store import SharedMemoryStore
        store = SharedMemoryStore(self.workspace, share_group_id)
        store.edit(memory_id, body)
        return {"ok": True, "memory_id": memory_id}

    def lock_memory(self, memory_id: str, share_group_id: str = "default") -> dict:
        """锁定记忆。"""
        from .shared_memory_store import SharedMemoryStore
        store = SharedMemoryStore(self.workspace, share_group_id)
        store.lock(memory_id)
        return {"ok": True, "memory_id": memory_id}

    def unlock_memory(self, memory_id: str, share_group_id: str = "default") -> dict:
        """解锁记忆。"""
        from .shared_memory_store import SharedMemoryStore
        store = SharedMemoryStore(self.workspace, share_group_id)
        store.unlock(memory_id)
        return {"ok": True, "memory_id": memory_id}

    def restore_memory(self, memory_id: str, share_group_id: str = "default") -> dict:
        """恢复 shadowed 记忆为 active。"""
        from .shared_memory_store import SharedMemoryStore
        store = SharedMemoryStore(self.workspace, share_group_id)
        store.restore(memory_id)
        return {"ok": True, "memory_id": memory_id}

    def delete_memory(self, memory_id: str, share_group_id: str = "default") -> dict:
        """软删除记忆。"""
        from .shared_memory_store import SharedMemoryStore
        store = SharedMemoryStore(self.workspace, share_group_id)
        store.delete(memory_id)
        return {"ok": True, "memory_id": memory_id}

    def rollback_memory(self, version_id: str, share_group_id: str = "default") -> dict:
        """回滚到指定版本。"""
        from .shared_memory_store import SharedMemoryStore
        store = SharedMemoryStore(self.workspace, share_group_id)
        store.rollback_to_version(version_id)
        return {"ok": True, "version_id": version_id}

    def list_memory_versions(self, share_group_id: str = "default") -> dict:
        """列出所有版本。"""
        from .shared_memory_store import SharedMemoryStore
        store = SharedMemoryStore(self.workspace, share_group_id)
        return {"versions": store.list_versions()}

    # ------------------------------------------------------------------
    # AutoOrganizeApi（v3.2 §8.2）：自动整理观察
    # ------------------------------------------------------------------

    def get_recent_events(self, share_group_id: str = "default") -> dict:
        """最近自动写入事件。"""
        from .shared_memory_store import SharedMemoryStore
        store = SharedMemoryStore(self.workspace, share_group_id)
        events = store.list_events()
        # 最近 50 条
        recent = events[-50:] if len(events) > 50 else events
        return {"events": [e.to_dict() for e in recent], "total": len(events)}

    def get_auto_actions(self, share_group_id: str = "default") -> dict:
        """自动整理记录（从 events 的 auto_actions 聚合）。"""
        from .shared_memory_store import SharedMemoryStore
        store = SharedMemoryStore(self.workspace, share_group_id)
        events = store.list_events()
        actions = []
        for e in events:
            for a in e.auto_actions:
                actions.append({**a, "event_id": e.event_id,
                               "agent": e.agent_instance_id, "created_at": e.created_at})
        return {"actions": actions, "total": len(actions)}

    def get_supersede_chain(self, memory_id: str,
                            share_group_id: str = "default") -> dict:
        """获取覆盖链。"""
        from .shared_memory_store import SharedMemoryStore
        store = SharedMemoryStore(self.workspace, share_group_id)
        record = store.get_record(memory_id)
        if record is None:
            return {"error": "memory not found"}
        chain = list(record.supersedes)
        # 递归查找
        all_records = store.list_records()
        for r in all_records:
            if memory_id in r.supersedes:
                chain.append(r.memory_id)
        return {"memory_id": memory_id, "supersedes": record.supersedes, "superseded_by": chain}

    def get_conflicts(self, share_group_id: str = "default") -> dict:
        """冲突队列。"""
        from .shared_memory_store import SharedMemoryStore
        store = SharedMemoryStore(self.workspace, share_group_id)
        conflicts = store.list_conflicts()
        return {"conflicts": [c.to_dict() for c in conflicts], "total": len(conflicts)}

    def get_quarantine(self, share_group_id: str = "default") -> dict:
        """隔离队列。"""
        from .shared_memory_store import SharedMemoryStore
        store = SharedMemoryStore(self.workspace, share_group_id)
        entries = store.list_quarantine()
        return {"quarantine": [e.to_dict() for e in entries], "total": len(entries)}

    def get_memory_status(self, share_group_id: str = "default") -> dict:
        """共享组状态统计。"""
        from .shared_memory_store import SharedMemoryStore
        store = SharedMemoryStore(self.workspace, share_group_id)
        return store.status()

    def get_supersede_decisions(self, share_group_id: str = "default") -> dict:
        """获取所有 auto_supersede 决策及关联记录内容预览。"""
        from .shared_memory_store import SharedMemoryStore
        store = SharedMemoryStore(self.workspace, share_group_id)
        decisions = store.list_decisions()
        records = {r.memory_id: r for r in store.list_records()}
        result = []
        for d in decisions:
            if d.action != "auto_supersede":
                continue
            target_ids = d.target_ids or []
            old_id = target_ids[0] if len(target_ids) > 0 else ""
            new_id = target_ids[1] if len(target_ids) > 1 else ""
            old_rec = records.get(old_id)
            new_rec = records.get(new_id)
            result.append({
                "decision_id": d.event_id,
                "old_memory_id": old_id,
                "new_memory_id": new_id,
                "old_content_preview": (old_rec.body if old_rec else "")[:100],
                "new_content_preview": (new_rec.body if new_rec else "")[:100],
                "reason": d.reason,
                "created_at": d.created_at,
            })
        return {"decisions": result, "total": len(result)}

    def resolve_conflict(self, group_id: str, keep_memory_id: str,
                         share_group_id: str = "default") -> dict:
        """解决冲突：保留指定记忆，其他成员软删除。"""
        from .shared_memory_store import SharedMemoryStore
        store = SharedMemoryStore(self.workspace, share_group_id)
        conflicts = store.list_conflicts()
        group = next((c for c in conflicts if c.group_id == group_id), None)
        if group is None:
            return {"error": "conflict group not found"}
        for mid in group.member_ids:
            if mid != keep_memory_id:
                store.delete(mid)
        store.restore(keep_memory_id)
        return {"ok": True, "kept": keep_memory_id}

    def release_quarantine(self, quarantine_id: str,
                           share_group_id: str = "default") -> dict:
        """释放隔离：恢复记忆为 active。"""
        from .shared_memory_store import SharedMemoryStore
        store = SharedMemoryStore(self.workspace, share_group_id)
        entries = store.list_quarantine()
        entry = next((e for e in entries if e.quarantine_id == quarantine_id), None)
        if entry is None:
            return {"error": "quarantine entry not found"}
        store.restore(entry.memory_id)
        return {"ok": True, "memory_id": entry.memory_id}

    def delete_quarantine(self, quarantine_id: str,
                          share_group_id: str = "default") -> dict:
        """永久删除隔离记忆。"""
        from .shared_memory_store import SharedMemoryStore
        store = SharedMemoryStore(self.workspace, share_group_id)
        entries = store.list_quarantine()
        entry = next((e for e in entries if e.quarantine_id == quarantine_id), None)
        if entry is None:
            return {"error": "quarantine entry not found"}
        store.delete(entry.memory_id)
        return {"ok": True, "memory_id": entry.memory_id}

    def _preview_source_impl(self, path: str, source_type: str = "selected_directory") -> dict:
        """v3.1 §1.1 P0：添加来源前必须先 preview。type 别名映射防止 ValueError。"""
        from .source_registry import SourceRegistry
        from .schema_v3 import SourceRootType
        type_alias = {
            "directory": SourceRootType.SELECTED_DIRECTORY,
            "selected_directory": SourceRootType.SELECTED_DIRECTORY,
            "file": SourceRootType.SELECTED_FILE,
            "selected_file": SourceRootType.SELECTED_FILE,
            "obsidian": SourceRootType.OBSIDIAN_VAULT,
            "obsidian_vault": SourceRootType.OBSIDIAN_VAULT,
        }
        enum_type = type_alias.get(source_type, SourceRootType.SELECTED_DIRECTORY)
        reg = SourceRegistry(self.workspace)
        return reg.preview(path, enum_type)

    def _add_source_impl(self, path: str, source_type: str = "selected_directory",
                         display_name: str = "", confirmed: bool = False) -> dict:
        """v3.1 §1.1 P0：type 别名映射 + confirmed 强制。"""
        if not confirmed:
            return {"error": "需要确认才能添加来源"}
        from .source_registry import SourceRegistry
        from .schema_v3 import SourceRootType
        type_alias = {
            "directory": SourceRootType.SELECTED_DIRECTORY,
            "selected_directory": SourceRootType.SELECTED_DIRECTORY,
            "file": SourceRootType.SELECTED_FILE,
            "selected_file": SourceRootType.SELECTED_FILE,
            "obsidian": SourceRootType.OBSIDIAN_VAULT,
            "obsidian_vault": SourceRootType.OBSIDIAN_VAULT,
        }
        enum_type = type_alias.get(source_type, SourceRootType.SELECTED_DIRECTORY)
        reg = SourceRegistry(self.workspace)
        root = reg.add(path, enum_type, display_name=display_name)
        return {"ok": True, "root_id": root.root_id}

    def preview_source(self, path: str, source_type: str = "selected_directory") -> dict:
        """v3.1 §1.1 P0：添加来源前必须先 preview，展示预计范围、文件数、排除项。"""
        return self._preview_source_impl(path, source_type)

    def add_source(self, path: str, source_type: str = "selected_directory",
                   display_name: str = "", confirmed: bool = False) -> dict:
        """v3.1 §1.1 P0：type 别名映射 + confirmed 强制。"""
        return self._add_source_impl(path, source_type, display_name, confirmed)

    def remove_source(self, source_id: str, confirmed: bool = False) -> dict:
        if not confirmed:
            return {"error": "需要确认才能删除来源"}
        from .source_registry import SourceRegistry
        reg = SourceRegistry(self.workspace)
        ok = reg.remove(source_id)
        return {"ok": ok}

    def scan_sources(self) -> dict:
        """执行扫描，返回快照 + 覆盖率。"""
        from .source_registry import SourceRegistry, ScanBudget
        reg = SourceRegistry(self.workspace)
        snap = reg.scan(ScanBudget())
        cov = snap.coverage.counts()
        cov["coverage_status"] = snap.coverage.status().value
        return {
            "snapshot_id": snap.snapshot_id,
            "created_at": snap.created_at,
            "source_object_count": len(snap.source_objects),
            "coverage": cov,
        }

    def get_raw_memory(self) -> dict:
        """返回原始记忆：按 agent（SourceRoot display_name）分组展示所有 SourceObject。

        spec §7.2 SourceApi：用户能直接看到每个 agent 的原始记忆文件，不做任何萃取。
        """
        from .source_registry import SourceRegistry, ScanBudget
        reg = SourceRegistry(self.workspace)
        snap = reg.scan(ScanBudget())
        # root_id -> display_name 映射
        root_map = {r.root_id: r for r in reg.list_sources()}
        groups: dict[str, dict] = {}
        for obj in snap.source_objects:
            root = root_map.get(obj.source_root_id)
            agent_name = root.display_name if root else obj.source_root_id
            group = groups.setdefault(agent_name, {
                "agent": agent_name,
                "root_id": obj.source_root_id,
                "root_path": root.path if root else "",
                "scope": root.scope if root else "unknown",
                "files": [],
            })
            group["files"].append({
                "relative_path": obj.relative_path,
                "media_type": obj.media_type,
                "content_hash": obj.content_hash,
                "read_status": obj.read_status,
                "captured_at": obj.captured_at,
            })
        # 加入覆盖率统计
        cov = snap.coverage.counts()
        cov["coverage_status"] = snap.coverage.status().value
        return {
            "snapshot_id": snap.snapshot_id,
            "created_at": snap.created_at,
            "groups": list(groups.values()),
            "group_count": len(groups),
            "total_files": len(snap.source_objects),
            "coverage": cov,
        }

    def get_source_file_content(self, root_id: str, relative_path: str) -> dict:
        """读取某个原始记忆文件的完整内容（只读，用于 UI 查看）。

        v3.1 §1.5 P0：必须做 canonical containment 和符号链接防护，
        防止 ../ 或越界 symlink 读取授权根之外的文件。
        """
        from .source_registry import SourceRegistry
        from pathlib import Path
        import os
        reg = SourceRegistry(self.workspace)
        root = reg.get(root_id)
        if root is None:
            return {"error": "source root not found"}
        root_path = Path(root.path).resolve()
        # canonical containment：resolve 后必须仍在 root_path 之内
        full = (root_path / relative_path).resolve()
        try:
            full.relative_to(root_path)
        except ValueError:
            return {"error": "path escapes source root (containment violation)"}
        if not full.exists() or not full.is_file():
            return {"error": "file not found"}
        # 符号链接防护：不允许 symlink 指向 root 之外
        if full.is_symlink():
            target = Path(os.readlink(full)).resolve() if os.readlink(full) else None
            if target is None:
                return {"error": "symlink target unreadable"}
            try:
                target.relative_to(root_path)
            except ValueError:
                return {"error": "symlink escapes source root"}
        # 文件大小限制（防止误读大文件）
        try:
            stat = full.stat()
            if stat.st_size > 5 * 1024 * 1024:  # 5MB
                return {"error": f"file too large ({stat.st_size} bytes, max 5MB)"}
        except OSError as e:
            return {"error": f"stat failed: {e}"}
        try:
            content = full.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            return {"error": f"read failed: {e}"}
        return {
            "root_id": root_id,
            "relative_path": relative_path,
            "display_name": root.display_name,
            "content": content,
            "size": len(content),
        }

    def _extract_source_file_memories(self, root_id: str, relative_path: str,
                                     share_group_id: str = "default",
                                     agent_instance_id: str = "document-extractor",
                                     max_segments: int = 20) -> dict:
        """[PRIVATE] 旧直接写入方法，已由 extract_preview + accept_candidates 两步流程替代。

        保留向后兼容，新代码应使用 extract_preview（只读预览）+ accept_candidates（确认写入）。
        """
        file_result = self.get_source_file_content(root_id, relative_path)
        if "error" in file_result:
            return file_result
        from .auto_organizer import AutoOrganizer
        from .schema_v3 import MemoryEvent, stable_hash, _now_iso
        from .shared_memory_store import SharedMemoryStore
        content = file_result.get("content", "")
        segments = self._extract_memory_segments(content, max_segments=max_segments)
        store = SharedMemoryStore(self.workspace, share_group_id)
        organizer = AutoOrganizer(self.workspace, share_group_id)
        extracted = []
        for idx, segment in enumerate(segments):
            event = MemoryEvent(
                event_id=stable_hash("doc_extract_event", root_id, relative_path, str(idx), segment, _now_iso()),
                agent_instance_id=agent_instance_id,
                share_group_id=share_group_id,
                raw_content=segment,
                metadata={
                    "source_root_id": root_id,
                    "relative_path": relative_path,
                    "extraction_origin": "source_file",
                },
                auto_actions=[],
                created_at=_now_iso(),
            )
            store.append_event(event)
            record, actions = organizer.organize(event)
            event.auto_actions = actions
            store.update_event(event)
            extracted.append({
                "memory_id": record.memory_id,
                "body": record.body,
                "kind": record.kind.value,
                "status": record.status.value,
                "auto_actions": actions,
            })
        return {
            "ok": True,
            "root_id": root_id,
            "relative_path": relative_path,
            "share_group_id": share_group_id,
            "document_promoted_as_memory": False,
            "extracted": extracted,
            "total": len(extracted),
        }

    # ------------------------------------------------------------------
    # §8.5 两步萃取流程：extract_preview（只读）-> accept_candidates（写入）
    # ------------------------------------------------------------------

    def extract_preview(self, root_id: str, relative_path: str,
                        max_segments: int = 20) -> dict:
        """§8.5 步骤 1：萃取预览（只读，不写入 SharedMemoryStore）。

        提取文档片段、分类、风险扫描，返回候选列表。
        候选缓存到 .memoryguard/staging/extract-{hash}.json 供 accept_candidates 引用。
        """
        import json
        import time
        from pathlib import Path
        from .auto_organizer import AutoOrganizer
        from .schema_v3 import stable_hash, _now_iso

        file_result = self.get_source_file_content(root_id, relative_path)
        if "error" in file_result:
            return file_result
        content = file_result.get("content", "")
        segments = self._extract_memory_segments(content, max_segments=max_segments)

        # 用 AutoOrganizer 的只读方法做分类 + 风险扫描（不调 organize，避免写入）
        organizer = AutoOrganizer(self.workspace, "default")
        candidates = []
        for idx, segment in enumerate(segments):
            kind = organizer._classify(segment)
            confidence = organizer._confidence(segment, kind)
            secret = organizer._detect_secret(segment)
            if secret:
                risk_level = "high"
            elif confidence < 0.45:
                risk_level = "medium"
            else:
                risk_level = "low"
            # candidate_id 稳定：同一文档同一片段每次萃取 ID 相同（不含时间戳）
            candidate_id = stable_hash("candidate", root_id, relative_path, str(idx), segment)
            candidates.append({
                "candidate_id": candidate_id,
                "body": segment,
                "kind": kind.value,
                "risk_level": risk_level,
                "preview": segment[:200],
            })

        # 生成 extract_id 并缓存到 staging 文件
        extract_id = stable_hash("extract", root_id, relative_path, _now_iso())
        staging_dir = Path(self.workspace) / ".memoryguard" / "staging"
        staging_dir.mkdir(parents=True, exist_ok=True)

        # 清理过期 staging 文件（>24h）
        cutoff = time.time() - 24 * 3600
        for f in staging_dir.glob("extract-*.json"):
            try:
                if f.stat().st_mtime < cutoff:
                    f.unlink()
            except OSError:
                continue

        staging_file = staging_dir / f"extract-{extract_id}.json"
        staging_data = {
            "extract_id": extract_id,
            "root_id": root_id,
            "relative_path": relative_path,
            "created_at": _now_iso(),
            "candidates": candidates,
        }
        staging_file.write_text(json.dumps(staging_data, ensure_ascii=False, indent=2), encoding="utf-8")

        return {
            "ok": True,
            "extract_id": extract_id,
            "root_id": root_id,
            "relative_path": relative_path,
            "candidates": candidates,
            "total": len(candidates),
        }

    def accept_candidates(self, extract_id: str, candidate_ids: list[str],
                          share_group_id: str = "default",
                          agent_instance_id: str = "document-extractor") -> dict:
        """§8.5 步骤 2：接受候选（写入 SharedMemoryStore，需用户确认）。

        读取 staging 文件，只接受 candidate_ids 中的候选，写入后删除 staging 文件。
        """
        import json
        from pathlib import Path
        from .auto_organizer import AutoOrganizer
        from .schema_v3 import MemoryEvent, DecisionEvent, stable_hash, _now_iso
        from .shared_memory_store import SharedMemoryStore

        staging_dir = Path(self.workspace) / ".memoryguard" / "staging"
        staging_file = staging_dir / f"extract-{extract_id}.json"
        if not staging_file.exists():
            return {"error": f"staging file not found (extract_id={extract_id}); it may have expired"}

        staging_data = json.loads(staging_file.read_text(encoding="utf-8"))
        all_candidates = staging_data.get("candidates", [])
        candidate_map = {c["candidate_id"]: c for c in all_candidates}
        accepted = [candidate_map[cid] for cid in candidate_ids if cid in candidate_map]
        if not accepted:
            return {"error": "no matching candidates found in staging file"}

        root_id = staging_data.get("root_id", "")
        relative_path = staging_data.get("relative_path", "")

        store = SharedMemoryStore(self.workspace, share_group_id)
        organizer = AutoOrganizer(self.workspace, share_group_id)
        results = []
        written_ids = []
        for candidate in accepted:
            segment = candidate["body"]
            event = MemoryEvent(
                event_id=stable_hash("doc_extract_event", root_id, relative_path,
                                     candidate["candidate_id"], segment, _now_iso()),
                agent_instance_id=agent_instance_id,
                share_group_id=share_group_id,
                raw_content=segment,
                metadata={
                    "source_root_id": root_id,
                    "relative_path": relative_path,
                    "extraction_origin": "source_file",
                    "candidate_id": candidate["candidate_id"],
                },
                auto_actions=[],
                created_at=_now_iso(),
            )
            store.append_event(event)
            record, actions = organizer.organize(event)
            event.auto_actions = actions
            store.update_event(event)
            written_ids.append(record.memory_id)
            results.append({
                "memory_id": record.memory_id,
                "status": record.status.value,
                "kind": record.kind.value,
                "auto_actions": actions,
            })

        # 记录 DecisionEvent
        decision = DecisionEvent(
            event_id=stable_hash("accept_extract", extract_id, _now_iso()),
            actor="user",
            action="accept_extract",
            target_ids=written_ids,
            reason="user confirmed",
            created_at=_now_iso(),
        )
        store.append_decision(decision)

        # 写入完成后删除 staging 文件
        try:
            staging_file.unlink()
        except OSError:
            pass

        return {
            "ok": True,
            "extract_id": extract_id,
            "share_group_id": share_group_id,
            "accepted": results,
            "total": len(results),
        }

    def _extract_memory_segments(self, content: str, max_segments: int = 20) -> list[str]:
        import re
        blocks = []
        current: list[str] = []
        for line in content.splitlines():
            stripped = line.strip()
            if not stripped:
                if current:
                    blocks.append("\n".join(current).strip())
                    current = []
                continue
            if stripped.startswith("#") and current:
                blocks.append("\n".join(current).strip())
                current = [stripped]
            else:
                current.append(stripped)
        if current:
            blocks.append("\n".join(current).strip())
        candidates = []
        signal = re.compile(r"偏好|喜欢|习惯|步骤|流程|项目|事实|规则|必须|不要|应该|prefer|like|procedure|step|project|must|should", re.I)
        for block in blocks:
            clean = block.strip()
            if len(clean) < 8:
                continue
            if signal.search(clean) or clean.startswith("#"):
                candidates.append(clean[:1200])
            if len(candidates) >= max_segments:
                break
        if not candidates and content.strip():
            candidates.append(content.strip()[:1200])
        return candidates

    # ------------------------------------------------------------------
    # ImportApi（spec §7.2）
    # ------------------------------------------------------------------

    def preview_import(self, path: str) -> dict:
        from .adapters import GenericImportAdapter, ChatGPTImportAdapter
        from pathlib import Path
        bundle = Path(path)
        if not bundle.exists():
            return {"error": "bundle not found"}
        for ad in (ChatGPTImportAdapter(), GenericImportAdapter()):
            d = ad.detect(bundle)
            if d.supported:
                inv = ad.inventory(bundle)
                return {"provider": d.provider, "confidence": d.confidence,
                        "notes": d.notes, "inventory": inv}
        return {"error": "unsupported bundle format"}

    def create_import(self, path: str, confirmed: bool = False) -> dict:
        if not confirmed:
            return {"error": "需要确认才能创建导入"}
        from .adapters import GenericImportAdapter, ChatGPTImportAdapter
        from pathlib import Path
        bundle = Path(path)
        if not bundle.exists():
            return {"error": "bundle not found"}
        for ad in (ChatGPTImportAdapter(), GenericImportAdapter()):
            d = ad.detect(bundle)
            if d.supported:
                convs = ad.parse(bundle)
                records = ad.normalize(convs)
                return {"provider": d.provider,
                        "conversation_count": len(convs),
                        "memory_record_count": len(records)}
        return {"error": "unsupported bundle format"}

    # ------------------------------------------------------------------
    # MemoryApi（spec §7.2）
    # ------------------------------------------------------------------

    def get_memory_ir(self) -> dict:
        """读取当前 Memory IR。"""
        from .memory_ir import MemoryNormalizer
        norm = MemoryNormalizer(self.workspace)
        ir = norm.load()
        if ir is None:
            return {"empty": True, "reason": "not_built"}
        return {
            "records": [r.to_dict() for r in ir.records],
            "duplicate_groups": [g.to_dict() for g in ir.duplicate_groups],
            "snapshot_id": ir.snapshot_id,
            "record_count": len(ir.records),
        }

    def create_build_plan(self, target_path: str = "") -> dict:
        from .adapters import GenericMarkdownTarget
        from .release_manager import ReleaseManager
        from .source_registry import ScanBudget
        from pathlib import Path
        rm = ReleaseManager(self.workspace)
        target = GenericMarkdownTarget()
        tp = Path(target_path) if target_path else Path(self.workspace) / ".memoryguard" / "memory-target"
        snap, ir = rm.scan_and_normalize(ScanBudget())
        plan = rm.create_build_plan(ir, target, tp)
        return plan.to_dict()

    def apply_build(self, plan_id: str, confirmed: bool = False,
                    target_path: str = "") -> dict:
        if not confirmed:
            return {"error": "需要确认才能应用构建"}
        from .adapters import GenericMarkdownTarget
        from .release_manager import ReleaseManager
        from pathlib import Path
        rm = ReleaseManager(self.workspace)
        target = GenericMarkdownTarget()
        tp = Path(target_path) if target_path else Path(self.workspace) / ".memoryguard" / "memory-target"
        release = rm.apply_build(plan_id, target, tp, approval=True)
        return release.to_dict()

    def verify_release(self, release_id: str, target_path: str = "") -> dict:
        from .adapters import GenericMarkdownTarget
        from .release_manager import ReleaseManager
        from pathlib import Path
        import json
        rm = ReleaseManager(self.workspace)
        target = GenericMarkdownTarget()
        tp = Path(target_path) if target_path else Path(self.workspace) / ".memoryguard" / "memory-target"
        # 读 manifest
        change_path = Path(self.workspace) / ".memoryguard" / "changes" / f"{release_id}.json"
        if not change_path.exists():
            return {"error": "release not found"}
        data = json.loads(change_path.read_text(encoding="utf-8"))
        build_id = data.get("build_id", "")
        # 找 plan
        plans_dir = Path(self.workspace) / ".memoryguard" / "plans"
        manifest = None
        for pf in plans_dir.glob("*.json"):
            pd = json.loads(pf.read_text(encoding="utf-8"))
            if pd.get("manifest", {}).get("build_id") == build_id:
                manifest = pd["manifest"]
                break
        if manifest is None:
            return {"error": "manifest not found"}
        from .schema_v3 import BuildManifest
        mm = BuildManifest(
            build_id=manifest["build_id"], release_hash=manifest.get("release_hash", ""),
            target_profile=manifest.get("target_profile", ""),
        )
        return rm.verify_release(release_id, target, tp, mm)

    def rollback_release(self, release_id: str, confirmed: bool = False,
                         target_path: str = "") -> dict:
        if not confirmed:
            return {"error": "需要确认才能回滚"}
        from .adapters import GenericMarkdownTarget
        from .release_manager import ReleaseManager
        from pathlib import Path
        rm = ReleaseManager(self.workspace)
        target = GenericMarkdownTarget()
        tp = Path(target_path) if target_path else Path(self.workspace) / ".memoryguard" / "memory-target"
        rb = rm.rollback_release(release_id, target, tp)
        return rb.to_dict()

    def list_releases(self) -> dict:
        from .release_manager import ReleaseManager
        rm = ReleaseManager(self.workspace)
        return {"releases": rm.list_releases()}

    def list_history(self) -> dict:
        """v3.1 §8.4：统一历史时间线（rule_change + memory_release + warnings）。

        损坏 JSON 不会让页面崩溃，会在 warnings 中显示。
        """
        from .change_history import list_change_history
        from pathlib import Path
        return list_change_history(Path(self.workspace))

    # ------------------------------------------------------------------
    # 规则级修复闭环（v2.1 保留）
    # ------------------------------------------------------------------

    def get_audit(self) -> dict:
        """返回当前审计报告（dict）。若无则先跑一次。"""
        if self._report is None:
            self._report = self.run_audit()
        return self._report

    def run_audit(self) -> dict:
        """执行只读扫描 + 规则引擎，返回 Report dict。"""
        from .cli import run_audit

        report = run_audit(Path(self.workspace))
        self._report = report.to_dict()
        return self._report

    def generate_plan(self, finding_id: str) -> dict:
        """为指定 Finding 生成修复 Plan。"""
        import json
        from .cli import PLANS_DIR, _generate_patch, _load_report
        from .schema import Plan, RiskLevel, stable_id

        report = _load_report(Path(self.workspace))
        if report is None:
            return {"error": "no report found"}
        finding = next((f for f in report.findings if f.id == finding_id), None)
        if finding is None:
            return {"error": f"finding not found: {finding_id}"}
        if not finding.fixable:
            return {"error": "finding not fixable"}

        from .schema import Patch, sha256_file

        patch = _generate_patch(finding)
        if patch is None:
            return {"error": "could not generate patch"}

        risk = RiskLevel.HIGH if finding.severity.value in ("high", "critical") else RiskLevel.LOW
        plan = Plan(
            plan_id=stable_id("plan", finding_id),
            finding_ids=[finding_id],
            intent=f"fix {finding.rule_id}",
            risk_level=risk,
            patches=[patch],
            created_at=__import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
            preconditions=[f"file hash matches: {patch.before_hash}"],
            verification=[finding.verification],
            requires_approval=True,
        )
        # 写 plan 文件
        ws = Path(self.workspace)
        (ws / PLANS_DIR).mkdir(parents=True, exist_ok=True)
        plan_path = ws / PLANS_DIR / f"{plan.plan_id}.json"
        plan_path.write_text(json.dumps(plan.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")
        return {"plan": plan.to_dict()}

    def apply_plan(self, plan_id: str) -> dict:
        """应用 Plan: 备份 + 补丁 + 重扫验证。"""
        import json
        from .cli import (
            PLANS_DIR, CHANGES_DIR, BACKUPS_DIR, REPORTS_DIR, run_audit,
        )
        from .schema import (
            Change, ChangeStatus, Patch, Plan, RiskLevel, now_iso,
            sha256_file, stable_id,
        )

        ws = Path(self.workspace)
        plan_path = ws / PLANS_DIR / f"{plan_id}.json"
        if not plan_path.exists():
            return {"error": f"plan not found: {plan_id}"}
        plan_dict = json.loads(plan_path.read_text(encoding="utf-8"))
        plan = Plan(
            plan_id=plan_dict["plan_id"],
            finding_ids=plan_dict["finding_ids"],
            intent=plan_dict["intent"],
            risk_level=RiskLevel(plan_dict["risk_level"]),
            patches=[Patch(**p) for p in plan_dict["patches"]],
            created_at=plan_dict.get("created_at", ""),
            preconditions=plan_dict.get("preconditions", []),
            verification=plan_dict.get("verification", []),
            requires_approval=plan_dict.get("requires_approval", True),
        )

        # 校验 hash
        for patch in plan.patches:
            current = sha256_file(Path(patch.path))
            if current != patch.before_hash:
                return {"error": f"file changed: {patch.path}"}

        # 备份 + 应用
        (ws / BACKUPS_DIR).mkdir(parents=True, exist_ok=True)
        (ws / CHANGES_DIR).mkdir(parents=True, exist_ok=True)
        backup_paths, changed_paths = [], []
        for patch in plan.patches:
            src = Path(patch.path)
            backup = ws / BACKUPS_DIR / f"{src.name}.{stable_id('bak', patch.path)[:8]}"
            backup.write_bytes(src.read_bytes())
            backup_paths.append(str(backup))
            if patch.operation == "delete":
                src.unlink()
            elif patch.operation == "insert":
                content = src.read_text(encoding="utf-8")
                src.write_text(patch.diff.lstrip("+ ") + "\n" + content, encoding="utf-8")
            elif patch.operation == "replace":
                src.write_text(patch.diff, encoding="utf-8")
            changed_paths.append(patch.path)

        # 重扫验证
        verify_report = run_audit(ws)
        remaining = [f for f in verify_report.findings if f.id in plan.finding_ids]
        status = ChangeStatus.VERIFIED if not remaining else ChangeStatus.FAILED

        change = Change(
            change_id=stable_id("change", plan.plan_id),
            plan_id=plan.plan_id,
            applied_at=now_iso(),
            backup_paths=backup_paths,
            changed_paths=changed_paths,
            status=status,
        )
        (ws / CHANGES_DIR / f"{change.change_id}.json").write_text(
            json.dumps(change.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
        )
        # 刷新 report
        self._report = verify_report.to_dict()
        return {"change": change.to_dict()}

    def undo_change(self, change_id: str) -> dict:
        """撤销 Change: 从备份恢复 + 重扫。"""
        import json
        from .cli import CHANGES_DIR, run_audit
        from .schema import ChangeStatus

        ws = Path(self.workspace)
        change_path = ws / CHANGES_DIR / f"{change_id}.json"
        if not change_path.exists():
            return {"error": f"change not found: {change_id}"}
        change_dict = json.loads(change_path.read_text(encoding="utf-8"))
        for backup_path, changed_path in zip(change_dict["backup_paths"], change_dict["changed_paths"]):
            Path(changed_path).write_bytes(Path(backup_path).read_bytes())
        change_dict["status"] = ChangeStatus.UNDONE.value
        change_path.write_text(json.dumps(change_dict, ensure_ascii=False, indent=2), encoding="utf-8")
        # 刷新 report
        report = run_audit(ws)
        self._report = report.to_dict()
        return {"ok": True}


def open_interactive_window(workspace: str, title: str = "MemoryGuard 治理面板") -> int:
    """打开交互式治理面板（非平面报告）。

    通过 pywebview js_api 暴露 GovernanceApi，前端 JS 可调 audit/plan/apply/undo。
    使用本地文件模式（url=）而非内联 HTML（html=），以便加载 Cytoscape.js 等本地 JS 库。
    返回退出码：0 成功，3 pywebview 不可用。
    """
    if not has_native_gui():
        return 3
    import shutil
    import webview
    from .interactive import render_interactive_html

    api = GovernanceApi(workspace)
    html = render_interactive_html()

    # 写 HTML + cytoscape.js 到 .memoryguard/ui/ 目录，用 url= 加载本地文件
    ui_dir = Path(workspace) / ".memoryguard" / "ui"
    ui_dir.mkdir(parents=True, exist_ok=True)
    # 复制 cytoscape.js
    static_src = Path(__file__).parent / "static" / "cytoscape.min.js"
    if static_src.exists():
        shutil.copy2(static_src, ui_dir / "cytoscape.min.js")
    # 写 HTML
    html_path = ui_dir / "index.html"
    html_path.write_text(html, encoding="utf-8")

    window = webview.create_window(
        title, url=str(html_path), js_api=api,
        width=1200, height=800, min_size=(800, 600),
    )
    # v3.1：注入 window 引用，使 pick_path 能调用 create_file_dialog
    api._set_window(window)
    webview.start()
    return 0
