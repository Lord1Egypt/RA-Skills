from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
import requests
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_URL = "https://quantapi.51ifind.com/api/v1"


class IFindAPI:
    def __init__(self, refresh_token: str):
        self.refresh_token = refresh_token
        self.access_token: Optional[str] = None
        self.access_token_expires: Optional[datetime] = None

    def get_access_token(self) -> str:
        if self.access_token and self.access_token_expires:
            if datetime.now() < self.access_token_expires - timedelta(hours=1):
                return self.access_token

        headers = {
            "refresh_token": self.refresh_token,
            "Content-Type": "application/json",
        }

        response = requests.post(
            f"{BASE_URL}/get_access_token", headers=headers, timeout=30
        )
        response.raise_for_status()
        result = response.json()
        if result.get("errorcode") == 0:
            self.access_token = result.get("data", {}).get("access_token")
            self.access_token_expires = datetime.now() + timedelta(days=6)
            logger.info("成功获取access_token,有效期至: %s", self.access_token_expires)
            return self.access_token
        raise RuntimeError(f"获取access_token失败: {result.get('errmsg')}")

    def update_access_token(self) -> str:
        headers = {
            "refresh_token": self.refresh_token,
            "Content-Type": "application/json",
        }
        response = requests.post(
            f"{BASE_URL}/update_access_token", headers=headers, timeout=30
        )
        response.raise_for_status()
        result = response.json()
        if result.get("errorcode") == 0:
            self.access_token = result.get("data", {}).get("access_token")
            self.access_token_expires = datetime.now() + timedelta(days=6)
            logger.info("成功更新access_token,有效期至: %s", self.access_token_expires)
            return self.access_token
        raise RuntimeError(f"更新access_token失败: {result.get('errmsg')}")

    def _call_api(
        self, endpoint: str, payload: Dict[str, Any], max_retries: int = 3
    ) -> Dict[str, Any]:
        token = self.get_access_token()
        headers = {"access_token": token, "Content-Type": "application/json"}
        url = f"{BASE_URL}/{endpoint}"

        for attempt in range(max_retries):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=60)
                response.raise_for_status()
                result = response.json()

                if result.get("errorcode") == 0:
                    return result

                error_msg = result.get("errmsg", "未知错误")
                logger.warning("API调用失败: %s", error_msg)
                if "token" in error_msg.lower() or "expired" in error_msg.lower():
                    self.access_token = None
                    self.access_token_expires = None
                    token = self.get_access_token()
                    headers["access_token"] = token

                if attempt < max_retries - 1:
                    time.sleep(2**attempt)
                    continue
                raise RuntimeError(f"API调用失败: {error_msg}")

            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    time.sleep(2**attempt)
                    continue
                raise
            except requests.exceptions.RequestException:
                if attempt < max_retries - 1:
                    time.sleep(2**attempt)
                    continue
                raise

        raise RuntimeError("API调用失败,已达到最大重试次数")

    def get_basic_data(self, codes: str, indipara: List[Dict[str, Any]]) -> Dict[str, Any]:
        return self._call_api("basic_data_service", {"codes": codes, "indipara": indipara})

    def get_date_sequence(
        self,
        codes: str,
        startdate: str,
        enddate: str,
        indipara: Optional[List[Dict[str, Any]]] = None,
        functionpara: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload = {"codes": codes, "startdate": startdate, "enddate": enddate}
        if indipara:
            payload["indipara"] = indipara
        if functionpara:
            payload["functionpara"] = functionpara
        return self._call_api("date_sequence", payload)

    def get_history_data(
        self,
        codes: str,
        startdate: str,
        enddate: str,
        indicators: str,
        functionpara: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload = {
            "reqBody": {
                "codes": codes,
                "startdate": startdate,
                "enddate": enddate,
                "indicators": indicators,
            }
        }
        if functionpara:
            payload["reqBody"]["functionpara"] = functionpara
        return self._call_api("history_data", payload)

    def get_high_frequency(
        self,
        codes: str,
        indicators: str,
        starttime: str,
        endtime: str,
        functionpara: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload = {
            "codes": codes,
            "indicators": indicators,
            "starttime": starttime,
            "endtime": endtime,
        }
        if functionpara:
            payload["functionpara"] = functionpara
        return self._call_api("high_frequency", payload)

    def get_real_time_quotation(self, codes: str, indicators: str, functionpara: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = {"codes": codes, "indicators": indicators}
        if functionpara:
            payload["functionpara"] = functionpara
        return self._call_api("real_time_quotation", payload)

    def get_snap_shot(self, codes: str, indicators: str, starttime: str, endtime: str) -> Dict[str, Any]:
        return self._call_api("snap_shot", {"codes": codes, "indicators": indicators, "starttime": starttime, "endtime": endtime})

    def get_edb_data(self, indicators: str, startdate: str, enddate: str, functionpara: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        payload = {"reqBody": {"indicators": indicators, "startdate": startdate, "enddate": enddate}}
        if functionpara:
            payload["reqBody"]["functionpara"] = functionpara
        return self._call_api("edb_service", payload)

    def get_data_pool(self, reportname: str, functionpara: Dict[str, Any], outputpara: Optional[str] = None) -> Dict[str, Any]:
        payload = {"reqBody": {"reportname": reportname, "functionpara": functionpara}}
        if outputpara:
            payload["reqBody"]["outputpara"] = outputpara
        return self._call_api("data_pool", payload)

    def get_data_volume(self) -> Dict[str, Any]:
        token = self.get_access_token()
        headers = {"access_token": token, "Content-Type": "application/json"}
        response = requests.get(f"{BASE_URL}/get_data_volume", headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_error_message(self, errorcode: int) -> Dict[str, Any]:
        return self._call_api("get_error_message", {"reqBody": {"errorcode": errorcode}})

    def get_thscode(
        self,
        seccode: Optional[str] = None,
        secname: Optional[str] = None,
        mode: str = "seccode",
        sectype: str = "",
        market: str = "",
        tradestatus: str = "0",
        isexact: str = "0",
    ) -> Dict[str, Any]:
        functionpara = {
            "mode": mode,
            "sectype": sectype,
            "market": market,
            "tradestatus": tradestatus,
            "isexact": isexact,
        }
        payload = {"functionpara": functionpara}
        if seccode:
            payload["seccode"] = seccode
        if secname:
            payload["secname"] = secname
        return self._call_api("get_thscode", payload)

    def query_report(self, codes: str, functionpara: Optional[Dict[str, Any]] = None, outputpara: Optional[str] = None) -> Dict[str, Any]:
        payload = {"reqBody": {"codes": codes}}
        if functionpara:
            payload["reqBody"]["functionpara"] = functionpara
        if outputpara:
            payload["reqBody"]["outputpara"] = outputpara
        return self._call_api("report_query", payload)


class IFindHistoryData(IFindAPI):
    OHLC = "open,high,low,close"
    OHLCV = "open,high,low,close,volume"
    NO_ADJUST = "1"
    FORWARD_ADJUST = "2"
    BACKWARD_ADJUST = "3"
    DAILY = "D"
    WEEKLY = "W"
    MONTHLY = "M"

    def get_ohlc(self, codes: str, startdate: str, enddate: str, adjust: str = NO_ADJUST, period: str = DAILY) -> Dict[str, Any]:
        return self.get_history_data(
            codes=codes,
            startdate=startdate,
            enddate=enddate,
            indicators=self.OHLCV,
            functionpara={"CPS": adjust, "Interval": period},
        )


class IFindRealtimeData(IFindAPI):
    BASIC = "tradeDate,tradeTime,preClose,open,high,low,latest,avgPrice,change,changeRatio"

    def get_realtime(self, codes: str, indicators: Optional[str] = None) -> Dict[str, Any]:
        return self.get_real_time_quotation(codes, indicators or self.BASIC)
