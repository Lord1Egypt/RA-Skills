"""Thin HTTP client for DART OpenAPI."""
from __future__ import annotations

import io
import json
import os
import zipfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from xml.etree import ElementTree as ET

import requests

BASE_URL = "https://opendart.fss.or.kr/api"

# 공식 응답 status 코드 -> 한국어 메시지
_STATUS_MESSAGES = {
    "000": "정상",
    "010": "등록되지 않은 키입니다.",
    "011": "사용할 수 없는 키입니다. 오픈API 이용신청 후 승인을 받으십시오.",
    "012": "접근할 수 없는 IP입니다.",
    "013": "조회된 데이터가 없습니다.",
    "014": "파일이 존재하지 않습니다.",
    "020": "요청 제한을 초과하였습니다.",
    "021": "조회 가능한 회사수가 초과하였습니다.(최대 100건)",
    "100": "필드의 부적절한 값입니다. 필수값 확인 필요.",
    "101": "부적절한 접근입니다.",
    "800": "시스템 점검 중입니다.",
    "900": "정의되지 않은 오류가 발생하였습니다.",
    "901": "사용자 계정의 개인정보 보호 요청으로 인해 해당 API 서비스를 이용하실 수 없습니다.",
}


class OpenDartError(RuntimeError):
    """DART API가 000 외 상태를 반환했을 때 발생."""

    def __init__(self, status: str, message: str):
        super().__init__(f"[{status}] {message}")
        self.status = status
        self.message = message


class OpenDartClient:
    """Minimal wrapper for the DART OpenAPI."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        cache_dir: Optional[Path] = None,
        session: Optional[requests.Session] = None,
        timeout: float = 20.0,
    ) -> None:
        self.api_key = api_key or os.environ.get("OPENDART_API_KEY", "")
        if not self.api_key:
            raise OpenDartError(
                "AUTH",
                "OPENDART_API_KEY 환경 변수가 비어 있습니다. https://opendart.fss.or.kr 에서 키 발급 후 지정하세요.",
            )
        default_cache = Path(os.environ.get("OPENDART_CACHE_DIR", Path.home() / ".opendart-cli"))
        self.cache_dir = Path(cache_dir) if cache_dir else default_cache
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.session = session or requests.Session()
        self.timeout = timeout

    # ---------- low-level ----------
    def _get_json(self, path: str, **params: Any) -> Dict[str, Any]:
        params = {"crtfc_key": self.api_key, **{k: v for k, v in params.items() if v is not None}}
        url = f"{BASE_URL}/{path}"
        resp = self.session.get(url, params=params, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status")
        if status and status != "000":
            raise OpenDartError(status, _STATUS_MESSAGES.get(status, data.get("message", "unknown")))
        return data

    def _get_bytes(self, path: str, **params: Any) -> bytes:
        params = {"crtfc_key": self.api_key, **{k: v for k, v in params.items() if v is not None}}
        url = f"{BASE_URL}/{path}"
        resp = self.session.get(url, params=params, timeout=self.timeout, stream=True)
        resp.raise_for_status()
        content = resp.content
        # Some error responses come back as JSON even when a binary was expected.
        if content[:1] == b"{":
            try:
                data = json.loads(content)
                status = data.get("status")
                if status and status != "000":
                    raise OpenDartError(status, _STATUS_MESSAGES.get(status, data.get("message", "unknown")))
            except json.JSONDecodeError:
                pass
        return content

    # ---------- corp codes ----------
    def corp_code_cache_path(self) -> Path:
        return self.cache_dir / "corp_codes.json"

    def refresh_corp_codes(self) -> List[Dict[str, str]]:
        """Download the master ZIP, parse CORPCODE.xml, cache as JSON."""
        raw = self._get_bytes("corpCode.xml")
        try:
            zf = zipfile.ZipFile(io.BytesIO(raw))
        except zipfile.BadZipFile as exc:
            raise OpenDartError("ZIP", f"corpCode.xml 응답이 ZIP 형식이 아닙니다: {exc}") from exc
        xml_name = next((n for n in zf.namelist() if n.lower().endswith(".xml")), None)
        if not xml_name:
            raise OpenDartError("ZIP", "ZIP 내부에 XML이 없습니다.")
        root = ET.fromstring(zf.read(xml_name))
        rows: List[Dict[str, str]] = []
        for node in root.findall("./list"):
            rows.append(
                {
                    "corp_code": (node.findtext("corp_code") or "").strip(),
                    "corp_name": (node.findtext("corp_name") or "").strip(),
                    "stock_code": (node.findtext("stock_code") or "").strip(),
                    "modify_date": (node.findtext("modify_date") or "").strip(),
                }
            )
        self.corp_code_cache_path().write_text(
            json.dumps(rows, ensure_ascii=False), encoding="utf-8"
        )
        return rows

    def load_corp_codes(self, *, refresh: bool = False) -> List[Dict[str, str]]:
        path = self.corp_code_cache_path()
        if refresh or not path.exists():
            return self.refresh_corp_codes()
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return self.refresh_corp_codes()

    def find_corp(self, query: str, *, limit: int = 20) -> List[Dict[str, str]]:
        q = query.strip()
        rows = self.load_corp_codes()
        if q.isdigit() and len(q) == 6:
            matches = [r for r in rows if r["stock_code"] == q]
        elif q.isdigit() and len(q) == 8:
            matches = [r for r in rows if r["corp_code"] == q]
        else:
            matches = [r for r in rows if q in r["corp_name"]]
        return matches[:limit]

    # ---------- disclosure ----------
    def list_disclosures(
        self,
        *,
        corp_code: Optional[str] = None,
        bgn_de: Optional[str] = None,
        end_de: Optional[str] = None,
        last_reprt_at: Optional[str] = None,
        pblntf_ty: Optional[str] = None,
        corp_cls: Optional[str] = None,
        page_no: int = 1,
        page_count: int = 10,
    ) -> Dict[str, Any]:
        return self._get_json(
            "list.json",
            corp_code=corp_code,
            bgn_de=bgn_de,
            end_de=end_de,
            last_reprt_at=last_reprt_at,
            pblntf_ty=pblntf_ty,
            corp_cls=corp_cls,
            page_no=page_no,
            page_count=page_count,
        )

    def company(self, corp_code: str) -> Dict[str, Any]:
        return self._get_json("company.json", corp_code=corp_code)

    # ---------- finance ----------
    def finance(
        self,
        *,
        corp_code: str,
        bsns_year: str,
        reprt_code: str,
        fs_div: Optional[str] = None,
        full: bool = False,
    ) -> Dict[str, Any]:
        path = "fnlttSinglAcntAll.json" if full else "fnlttSinglAcnt.json"
        return self._get_json(
            path,
            corp_code=corp_code,
            bsns_year=bsns_year,
            reprt_code=reprt_code,
            fs_div=fs_div,
        )

    # ---------- shareholder ----------
    def major_stock(self, corp_code: str) -> Dict[str, Any]:
        return self._get_json("majorstock.json", corp_code=corp_code)

    def exec_stock(self, corp_code: str) -> Dict[str, Any]:
        return self._get_json("elestock.json", corp_code=corp_code)

    # ---------- document ----------
    def download_document(self, rcept_no: str) -> bytes:
        return self._get_bytes("document.xml", rcept_no=rcept_no)


def report_codes() -> Dict[str, str]:
    return {
        "11011": "사업보고서 (연간)",
        "11012": "반기보고서",
        "11013": "1분기보고서",
        "11014": "3분기보고서",
    }
