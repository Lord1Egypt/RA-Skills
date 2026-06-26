"""
禾连健康体检预约服务 - API接口封装
包含体检预约全流程的14个核心接口
"""
import requests
import json
import time
import base64
from typing import Optional, List, Dict, Any, Union
from dataclasses import dataclass, field


# ============== 基础配置 ==============
BASE_URL_WX = "https://healthcheck-web-client.helianhealth.com"
BASE_URL_MGMT = "https://management.helianhealth.com"
# BASE_URL_WX = "https://management-fed-gray.helianhealth.com/h2b3/healthcheck-web-client"
# BASE_URL_MGMT = "https://management-fed-gray.helianhealth.com/h2b3/healthmanage-web"

DEFAULT_HEADERS = {
    "Content-Type": "application/json",
}


# ============== 数据类定义 ==============
@dataclass
class ApiResponse:
    """API响应通用结构"""
    success: bool
    code: str
    error_msg: str
    result: Any
    raw_response: dict = field(default_factory=dict)
    
    @classmethod
    def from_dict(cls, data: dict) -> "ApiResponse":
        return cls(
            success=data.get("success", False),
            code=data.get("code", ""),
            error_msg=data.get("errorMsg", ""),
            result=data.get("result"),
            raw_response=data
        )
    
    @classmethod
    def error(cls, msg: str) -> "ApiResponse":
        return cls(
            success=False,
            code="-1",
            error_msg=msg,
            result=None,
            raw_response={}
        )


class HealthCheckService:
    """禾连健康体检预约服务"""
    
    def __init__(self, token: str = "", uid: str = ""):
        """
        初始化服务
        
        Args:
            token: 登录后获取的token（需登录的接口使用）
            uid: 登录后获取的用户ID（需登录的接口使用）
        """
        self.token = token
        self.uid = uid
        self.session = requests.Session()
    
    def set_auth(self, token: str, uid: str):
        """设置认证信息"""
        self.token = token
        self.uid = uid
    
    def _get_auth_headers(self) -> dict:
        """获取带认证的请求头"""
        headers = DEFAULT_HEADERS.copy()
        if self.token:
            headers["Token"] = self.token
        if self.uid:
            headers["Uid"] = self.uid
        return headers
    
    def _post(self, url: str, data: dict, need_auth: bool = False, use_json: bool = True) -> ApiResponse:
        """POST请求封装
        
        Args:
            url: 请求URL
            data: 请求数据
            need_auth: 是否需要认证
            use_json: 是否使用JSON格式，False则使用form-data
        """
        try:
            headers = self._get_auth_headers() if need_auth else DEFAULT_HEADERS.copy()
            if use_json:
                response = self.session.post(url, json=data, headers=headers, timeout=30)
            else:
                # 使用form-data格式，移除Content-Type头让requests自动设置
                if "Content-Type" in headers:
                    del headers["Content-Type"]
                response = self.session.post(url, data=data, headers=headers, timeout=30)
            response.raise_for_status()
            return ApiResponse.from_dict(response.json())
        except requests.RequestException as e:
            return ApiResponse.error(f"请求失败: {str(e)}")
        except json.JSONDecodeError as e:
            return ApiResponse.error(f"响应解析失败: {str(e)}")
    
    def _get(self, url: str, params: dict = None, need_auth: bool = False, return_raw: bool = False) -> Union[ApiResponse, bytes]:
        """GET请求封装"""
        try:
            headers = self._get_auth_headers() if need_auth else DEFAULT_HEADERS.copy()
            # GET请求不需要Content-Type为json
            if "Content-Type" in headers:
                del headers["Content-Type"]
            response = self.session.get(url, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            if return_raw:
                return response.content
            return ApiResponse.from_dict(response.json())
        except requests.RequestException as e:
            if return_raw:
                return b""
            return ApiResponse.error(f"请求失败: {str(e)}")
        except json.JSONDecodeError as e:
            if return_raw:
                return response.content
            return ApiResponse.error(f"响应解析失败: {str(e)}")

    # ============== Step 1: 查询区域代码 ==============
    def get_area_code_by_location(self, location_text: str) -> Optional[dict]:
        """
        根据用户输入的位置文本，匹配对应的市级区域代码。

        匹配规则：
        - 只匹配市级（level=2）
        - 支持"杭州"、"杭州市"、"杭州西湖"、"杭州西湖区"等格式
        - 自动处理带/不带"市"字的城市名称匹配

        Args:
            location_text: 用户输入的位置描述，如"杭州"、"杭州市"、"杭州西湖区"

        Returns:
            dict: {"area_code": int, "area_name": str, "level": int}
            或 None（完全无法匹配）
        """
        url = f"{BASE_URL_WX}/app/examination/institutions/allAreaV2"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception:
            return None

        result = data.get("result", [])

        # 只收集市级候选项
        city_candidates: List[dict] = []
        for province in result:
            if province.get("code") == 0:  # 跳过"推荐"分组
                continue
            for city in (province.get("children") or []):
                city_name = city.get("name", "")
                # 生成匹配变体："杭州市" -> ["杭州市", "杭州"]
                variants = [city_name]
                if city_name.endswith("市"):
                    variants.append(city_name[:-1])
                city_candidates.append({
                    "name": city_name,
                    "code": city["code"],
                    "variants": variants
                })

        # 遍历匹配：任一变体在 location_text 中即可
        for city in city_candidates:
            for variant in city["variants"]:
                if variant in location_text:
                    return {"area_code": city["code"], "area_name": city["name"], "level": 2}

        return None

    # ============== Step 1: 查询医院列表 ==============
    def get_hospital_list(
        self,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        area_code: Union[int, str] = 330100,
        page_no: int = 1,
        page_size: int = 10,
        is_from: int = 2,
        sort_type: int = 4,
        tag: int = 7,
        tag_list: List = None,
        version: int = 2,
        app_id: str = ""
    ) -> ApiResponse:
        """
        Step 1: 获取医院列表（无需登录）
        
        Args:
            latitude: 纹度，默认 None（不传经纬度时接口按 areaCode 查询）
            longitude: 经度，默认 None
            area_code: 区域代码，默认330100（杭州市）
            page_no: 页码，默认1
            page_size: 每页数量，默认10
            is_from: 来源，固定2
            sort_type: 排序类型，固定4
            tag: 标签，固定7
            tag_list: 标签列表，默认空
            version: 版本，固定2
            app_id: 应用ID，默认空
        
        Returns:
            ApiResponse: 包含医院列表
                result.list: 医院列表，每个医院包含:
                    - stationId: 医院ID
                    - stationName: 医院名称
                    - stationAddress: 医院地址
                    - distanceStr: 距离(km)
                    - salePrice: 最低价格
                result.total: 总数
        """
        url = f"{BASE_URL_WX}/wx/api/pkg/station/list"
        data = {
            "isFrom": is_from,
            "appId": app_id,
            "areaCode": area_code,
            "pageNo": page_no,
            "pageSize": page_size,
            "sortType": sort_type,
            "latitude": latitude,
            "longitude": longitude,
            "tag": tag,
            "tagList": tag_list or [],
            "version": version
        }
        return self._post(url, data)

    def get_hospital_list_with_branches(
        self,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        area_code: Union[int, str] = 330100,
        page_no: int = 1,
        page_size: int = 10,
        is_from: int = 2,
        sort_type: int = 4,
        tag: int = 7,
        tag_list: List = None,
        version: int = 2,
        app_id: str = ""
    ) -> ApiResponse:
        """
        Step 1 增强版: 获取医院列表并附带各医院的分院区信息（无需登录）
        
        内部先调用 get_hospital_list 获取医院列表，再并发调用 get_branch_list
        查询每家医院的分院区，将分院区信息合并到每个医院对象的 branches 字段中。

        Args:
            参数与 get_hospital_list 完全一致

        Returns:
            ApiResponse: 包含带分院区信息的医院列表
                result.list: 医院列表，每个医院在原有字段基础上新增:
                    - branches: 院区列表（数组），每个院区包含:
                        - branchId: 院区ID
                        - branchName: 院区名称
                        - branchAddress: 院区地址
                      若该医院无分院区，branches 为空列表 []
                result.total: 总数
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed

        # 1. 获取医院列表
        hospital_result = self.get_hospital_list(
            latitude=latitude,
            longitude=longitude,
            area_code=area_code,
            page_no=page_no,
            page_size=page_size,
            is_from=is_from,
            sort_type=sort_type,
            tag=tag,
            tag_list=tag_list,
            version=version,
            app_id=app_id
        )

        if not hospital_result.success:
            return hospital_result

        hospitals = hospital_result.result.get("list", [])
        if not hospitals:
            return hospital_result

        # 2. 并发查询每家医院的分院区
        def fetch_branches(hospital):
            station_id = hospital.get("stationId", "")
            if not station_id:
                return hospital, []
            branch_result = self.get_branch_list(station_id)
            branches = branch_result.result if branch_result.success and branch_result.result else []
            return hospital, branches

        with ThreadPoolExecutor(max_workers=min(len(hospitals), 5)) as executor:
            futures = {executor.submit(fetch_branches, h): h for h in hospitals}
            for future in as_completed(futures):
                hospital, branches = future.result()
                hospital["branches"] = branches

        return hospital_result

    # ============== Step 2: 查询套餐列表 ==============
    def get_package_list(
        self,
        station_id: str,
        page_no: int = 1,
        page_size: int = 10,
        is_from: int = 2,
        sort_type: int = 6,
        exclude_spu_ids: List = None,
        latitude: str = "",
        longitude: str = "",
        pkg_labels: List = None
    ) -> ApiResponse:
        """
        Step 2: 获取套餐列表（无需登录）
        
        Args:
            station_id: 医院ID（必填），格式如"HL123456"
            page_no: 页码，默认1
            page_size: 每页数量，默认10
            is_from: 来源，固定2
            sort_type: 排序类型，固定6
            exclude_spu_ids: 排除的套餐ID列表
            latitude: 纬度，默认空
            longitude: 经度，默认空
            pkg_labels: 套餐标签列表
        
        Returns:
            ApiResponse: 包含套餐列表
                result.list: 套餐列表，每个套餐包含:
                    - id: 套餐ID (spuId)
                    - goodsName: 套餐名称
                    - salePrice: 销售价格
                    - originalPrice: 原价
                    - itemCount: 检查项目数量
                result.total: 总数
        """
        url = f"{BASE_URL_WX}/wx/api/pkg/station/pkgList"
        data = {
            "stationId": station_id,
            "isFrom": is_from,
            "pageNo": page_no,
            "pageSize": page_size,
            "sortType": sort_type,
            "excludeSpuIds": exclude_spu_ids or [],
            "latitude": latitude,
            "longitude": longitude,
            "pkgLabels": pkg_labels or []
        }
        return self._post(url, data)

    # ============== Step 2 增强版: 套餐列表（含详情、号源与时间段） ==============
    def get_package_list_with_details(
        self,
        station_id: str,
        branch_id: Union[int, str] = "",
        page_no: int = 1,
        page_size: int = 10,
        max_dates: int = 10
    ) -> ApiResponse:
        """
        Step 2 增强版: 获取套餐列表并附带每个套餐的详情、可预约日期和时间段（无需登录）

        内部先调用 get_package_list 获取套餐列表，再并发调用 get_package_detail
        获取每个套餐的详情，接着并发查询每个套餐的可预约日期，对需要时间段的日期
        再并发查询时间段，最终将所有数据聚合到每个套餐对象中。

        Args:
            station_id: 医院ID（必填），格式如"HL123456"
            branch_id: 院区ID，无分院区传空字符串
            page_no: 页码，默认1
            page_size: 每页数量，默认10
            max_dates: 每个套餐最多展示的可预约日期数，默认10

        Returns:
            ApiResponse: 包含带详情和号源信息的套餐列表
                result.list: 套餐列表，每个套餐在原有字段基础上新增:
                    - detail: 套餐详情 { pkgInfo, skuInfo, instInfo }
                    - exam_names: 检查项目名称列表
                    - disease_names: 可筛查疾病名称列表
                    - item_ids: 检查项目ID列表
                    - available_dates: 可预约日期列表（前max_dates天），每个日期对象新增:
                        - time_slots: 时间段列表（仅 periodControlSwitch=true 时有值，否则为空列表）
                result.total: 总数
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed

        # 1. 获取套餐列表
        pkg_result = self.get_package_list(
            station_id=station_id,
            page_no=page_no,
            page_size=page_size
        )

        if not pkg_result.success:
            return pkg_result

        packages = pkg_result.result.get("list", [])
        if not packages:
            return pkg_result

        # 2. 并发查询每个套餐的详情
        def fetch_detail(pkg):
            spu_id = pkg.get("id")
            if not spu_id:
                return pkg, None
            detail_result = self.get_package_detail(spu_id=spu_id)
            if detail_result.success and detail_result.result:
                return pkg, detail_result.result
            return pkg, None

        with ThreadPoolExecutor(max_workers=min(len(packages), 5)) as executor:
            futures = {executor.submit(fetch_detail, p): p for p in packages}
            for future in as_completed(futures):
                pkg, detail = future.result()
                if detail:
                    pkg["detail"] = detail
                    pkg_info = detail.get("pkgInfo", {})
                    pkg["exam_names"] = parse_exam_item_names(pkg_info.get("examItemNewList", "[]"))
                    pkg["disease_names"] = parse_disease_names(pkg_info.get("diseaseJson", "[]"))
                    pkg["item_ids"] = parse_exam_item_ids(pkg_info.get("examItemNewList", ""))
                else:
                    pkg["detail"] = {}
                    pkg["exam_names"] = []
                    pkg["disease_names"] = []
                    pkg["item_ids"] = []

        # 3. 并发查询每个套餐的可预约日期
        def fetch_dates(pkg):
            detail = pkg.get("detail", {})
            pkg_info = detail.get("pkgInfo", {})
            pkg_id = pkg_info.get("pkgId")
            item_ids = pkg.get("item_ids", [])
            if not pkg_id or not item_ids:
                return pkg, []
            date_result = self.get_available_dates(
                station_id=station_id,
                pkg_id=pkg_id,
                item_ids=item_ids,
                branch_id=branch_id
            )
            if date_result.success and date_result.result:
                date_list = date_result.result.get("dateStampList") or []
                return pkg, date_list[:max_dates]
            return pkg, []

        with ThreadPoolExecutor(max_workers=min(len(packages), 5)) as executor:
            futures = {executor.submit(fetch_dates, p): p for p in packages}
            for future in as_completed(futures):
                pkg, dates = future.result()
                pkg["available_dates"] = dates

        # 4. 并发查询需要时间段的日期
        time_slot_tasks = []
        for pkg in packages:
            detail = pkg.get("detail", {})
            pkg_info = detail.get("pkgInfo", {})
            pkg_id = pkg_info.get("pkgId")
            item_ids = pkg.get("item_ids", [])
            for date_obj in pkg.get("available_dates", []):
                if date_obj.get("periodControlSwitch", False):
                    time_slot_tasks.append((pkg, date_obj, pkg_id, item_ids))
                else:
                    date_obj["time_slots"] = []

        if time_slot_tasks:
            def fetch_time_slots(task_info):
                pkg, date_obj, pkg_id, item_ids = task_info
                reserve_day = date_obj.get("reserveDay")
                if not reserve_day or not pkg_id:
                    return date_obj, []
                ts_result = self.get_available_time_slots(
                    reserve_day=reserve_day,
                    station_id=station_id,
                    pkg_id=pkg_id,
                    item_ids=item_ids,
                    branch_id=branch_id
                )
                if ts_result.success and ts_result.result:
                    return date_obj, ts_result.result.get("sectionList", [])
                return date_obj, []

            with ThreadPoolExecutor(max_workers=min(len(time_slot_tasks), 10)) as executor:
                futures = {executor.submit(fetch_time_slots, t): t for t in time_slot_tasks}
                for future in as_completed(futures):
                    date_obj, slots = future.result()
                    date_obj["time_slots"] = slots

        return pkg_result

    # ============== Step 3: 查询套餐详情 ==============
    def get_package_detail(
        self,
        spu_id: int,
        use_type: int = 30,
        latitude: str = "",
        longitude: str = ""
    ) -> ApiResponse:
        """
        Step 3: 获取套餐详情（无需登录）
        
        Args:
            spu_id: 套餐ID（必填，来自套餐列表的id字段）
            use_type: 使用类型，固定30
            latitude: 纬度，默认空
            longitude: 经度，默认空
        
        Returns:
            ApiResponse: 包含套餐详情
                result.pkgInfo: 套餐信息
                    - pkgId: 套餐ID（用于号源查询）
                    - pkgName: 套餐名称
                    - examItemNewList: 检查项目列表（JSON字符串，包含examFeeItemID）
                    - diseaseJson: 可筛查疾病（JSON字符串）
                result.skuInfo: SKU信息
                    - skuId: SKU ID（用于下单）
                    - salePrice: 销售价格
                    - goodsName: 商品名称
                result.instInfo: 医院信息
        """
        url = f"{BASE_URL_WX}/app/market/pkg/detail"
        params = {
            "spuId": spu_id,
            "useType": use_type,
            "latitude": latitude,
            "longitude": longitude
        }
        return self._get(url, params)

    # ============== Step 4: 查询院区列表 ==============
    def get_branch_list(self, station_id: str) -> ApiResponse:
        """
        Step 4: 获取分院区列表（无需登录）
        
        Args:
            station_id: 医院ID（必填）
        
        Returns:
            ApiResponse: 包含院区列表
                result: 院区列表（数组），每个院区包含:
                    - branchId: 院区ID
                    - branchName: 院区名称
                    - branchAddress: 院区地址
                若列表为空，表示无分院区
        """
        url = f"{BASE_URL_WX}/wx/api/inst/branch/list"
        params = {"stationId": station_id}
        return self._get(url, params)

    # ============== Step 5a: 查询可预约日期 ==============
    def get_available_dates(
        self,
        station_id: str,
        pkg_id: int,
        item_ids: List[str],
        branch_id: Union[int, str] = "",
        card_id: str = "",
        is_group: str = "0",
        upgrade_ids: List = None
    ) -> ApiResponse:
        """
        Step 5a: 获取可预约日期（无需登录）
        
        Args:
            station_id: 医院ID（必填）
            pkg_id: 套餐ID（必填，来自套餐详情的pkgInfo.pkgId）
            item_ids: 检查项目ID列表（必填，来自套餐详情的examFeeItemID列表）
            branch_id: 院区ID，无分院区传空字符串
            card_id: 卡ID，默认空
            is_group: 是否团体，固定"0"
            upgrade_ids: 升级ID列表
        
        Returns:
            ApiResponse: 包含可预约日期
                result.dateStampList: 日期列表，每个日期包含:
                    - reserveDay: 预约日期时间戳（秒）
                    - reserveDayStr: 日期字符串（如"20260311"）
                    - restCount: 剩余名额
                    - periodControlSwitch: 是否需要查询时间段
        """
        url = f"{BASE_URL_WX}/app/my/reserveBefore/userCanReserveGetInfo"
        data = {
            "stationId": station_id,
            "cardId": card_id,
            "isGroup": is_group,
            "itemIds": item_ids,
            "pkgId": pkg_id,
            "branchId": branch_id,
            "upgradeIds": upgrade_ids or []
        }
        return self._post(url, data)

    # ============== Step 5b: 查询可预约时间段 ==============
    def get_available_time_slots(
        self,
        reserve_day: int,
        station_id: str,
        pkg_id: int,
        item_ids: List[str] = None,
        branch_id: Union[int, str] = "",
        card_id: str = "",
        is_group: str = "0",
        reserve_id: str = "",
        trade_id: str = "",
        reserve_type: int = 0,
        upgrade_ids: List = None
    ) -> ApiResponse:
        """
        Step 5b: 获取可预约时间段（无需登录）
        
        仅当 periodControlSwitch=true 时需要调用此接口
        
        Args:
            reserve_day: 预约日期时间戳（秒级或毫秒级都支持）
            station_id: 医院ID（必填）
            pkg_id: 套餐ID（必填）
            item_ids: 检查项目ID列表
            branch_id: 院区ID，无分院区传空字符串
            card_id: 卡ID
            is_group: 是否团体，固定"0"
            reserve_id: 预约ID
            trade_id: 交易ID
            reserve_type: 预约类型
            upgrade_ids: 升级ID列表
        
        Returns:
            ApiResponse: 包含时间段列表
                result.sectionList: 时间段列表，每个时间段包含:
                    - showCheckTimeStr: 显示的时间段（如"05:00-05:30"）
                    - reserveCount: 剩余名额
                result.reserveInfo: 预约日期信息
        """
        url = f"{BASE_URL_WX}/app/my/reserveBefore/getIntervalTime"
        # 确保时间戳是毫秒级
        if reserve_day < 10000000000:
            reserve_day = reserve_day * 1000
        data = {
            "reserveDay": reserve_day,
            "stationId": station_id,
            "cardId": card_id,
            "branchId": branch_id,
            "isGroup": is_group,
            "pkgId": pkg_id,
            "itemIds": item_ids or [],
            "reserveId": reserve_id,
            "tradeId": trade_id,
            "reserveType": reserve_type,
            "upgradeIds": upgrade_ids or []
        }
        return self._post(url, data)

    # ============== Step 7a-1: 获取图形验证码 ==============
    def get_validate_code_image(self, phone: str) -> tuple:
        """
        Step 7a-1: 获取图形验证码（登录前置校验，无需登录）
        
        Args:
            phone: 手机号（必填）
        
        Returns:
            tuple: (成功标志, Base64图片数据或错误信息)
                成功时返回 (True, base64_image_string)
                失败时返回 (False, error_message)
        """
        url = f"{BASE_URL_MGMT}/wx/api/getValidateCode"
        params = {
            "device_id": phone,
            "t": int(time.time() * 1000)
        }
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            # 返回的是图片流，转换为Base64
            image_base64 = base64.b64encode(response.content).decode('utf-8')
            return True, image_base64
        except requests.RequestException as e:
            return False, f"获取验证码失败: {str(e)}"

    # ============== Step 7a-2: 发送短信验证码 ==============
    def send_sms_code(
        self,
        phone: str,
        validate_code: str,
        is_verify: str = "",
        station_id: str = ""
    ) -> ApiResponse:
        """
        Step 7a-2: 发送短信验证码（无需登录）
        
        必须先获取图形验证码并由用户输入后才能调用此接口
        
        Args:
            phone: 手机号（必填）
            validate_code: 图形验证码内容（必填，用户输入的图片中的数字）
            is_verify: 是否验证，默认空
            station_id: 医院ID，默认空
        
        Returns:
            ApiResponse: 发送结果
                result.sendOk: 是否发送成功
        """
        url = f"{BASE_URL_MGMT}/wx/api/smscode"
        params = {
            "cellphone": phone,
            "valiImgCode": validate_code,
            "isVerify": is_verify,
            "stationId": station_id
        }
        return self._get(url, params)

    # ============== Step 7a-3: 验证码登录 ==============
    def login_with_sms_code(self, phone: str, sms_code: str) -> ApiResponse:
        """
        Step 7a-3: 短信验证码登录
        
        Args:
            phone: 手机号（必填）
            sms_code: 短信验证码（必填，5位数字）
        
        Returns:
            ApiResponse: 登录结果
                result.token: 登录token（保存为 helianhealthcheck_token）
                result.userid: 用户ID（保存为 helianhealthcheck_uid）
                result.cellnumber: 手机号
                result.nick_name: 昵称
                result.real_name: 真实姓名
        """
        url = f"{BASE_URL_MGMT}/app/login/codeLogin"
        data = {
            "cellnumber": phone,
            "valicode": sms_code
        }
        response = self._post(url, data, use_json=False)
        
        # 如果登录成功，自动设置认证信息
        if response.success and response.result:
            self.set_auth(
                response.result.get("token", ""),
                response.result.get("userid", "")
            )
        
        return response

    # ============== Step 7b-1: 下单前校验-重复订单 ==============
    def check_repeat_order(
        self,
        age: int,
        card_no: str,
        gender: int,
        married: int,
        mobile: str,
        real_name: str,
        reserve_day: int,
        sku_ids: List[int],
        station_id: str,
        pay_amount: str,
        branch_id: Union[int, str] = 0,
        birthday: str = "",
        trade_type: str = "200",
        exampackage_pkg_id: Any = None,
        is_group: str = "0",
        pack_dp_list: List = None,
        check_time: str = ""
    ) -> ApiResponse:
        """
        Step 7b-1: 下单前校验-验证是否重复提交（需要登录）
        
        Args:
            age: 年龄（根据身份证计算）
            card_no: 身份证号
            gender: 性别（1=男, 2=女）
            married: 婚姻状态（0=未婚, 1=已婚）
            mobile: 手机号
            real_name: 姓名
            reserve_day: 预约日期时间戳（毫秒）
            sku_ids: SKU ID列表
            station_id: 医院ID
            pay_amount: 支付金额
            branch_id: 院区ID，无分院区传0
            birthday: 生日，默认空
            trade_type: 交易类型，固定"200"
            exampackage_pkg_id: 体检包ID
            is_group: 是否团体，固定"0"
            pack_dp_list: 包列表
            check_time: 时间段（如"05:00-05:30"）
        
        Returns:
            ApiResponse: 校验结果
                result: false表示未重复，可以继续下单
        """
        url = f"{BASE_URL_WX}/wx/api/market/trade/repeatOrder"
        # 确保时间戳是毫秒级
        if reserve_day < 10000000000:
            reserve_day = reserve_day * 1000
        data = {
            "age": age,
            "birthday": birthday,
            "branchId": branch_id,
            "cardNo": card_no,
            "gender": gender,
            "married": married,
            "mobile": mobile,
            "realName": real_name,
            "reserveDay": reserve_day,
            "skuIds": sku_ids,
            "stationId": station_id,
            "payAmount": pay_amount,
            "tradeType": trade_type,
            "exampackagePkgId": exampackage_pkg_id,
            "isGroup": is_group,
            "packDpList": pack_dp_list or [],
            "checkTime": check_time
        }
        return self._post(url, data, need_auth=True)

    # ============== Step 7b-2: 下单前校验-性别 ==============
    def check_gender_match(
        self,
        gender: int,
        user_gender: int,
        card_no: str,
        sku_id: int,
        optional_item_sku_ids: str = ""
    ) -> ApiResponse:
        """
        Step 7b-2: 下单前校验-验证性别（需要登录）
        
        Args:
            gender: 套餐要求的性别（1=男, 2=女）
            user_gender: 用户性别（1=男, 2=女）
            card_no: 身份证号
            sku_id: SKU ID
            optional_item_sku_ids: 可选项目SKU ID
        
        Returns:
            ApiResponse: 校验结果
                result: true表示性别匹配，可以继续下单
        """
        url = f"{BASE_URL_WX}/app/my/reserveBefore/genderMatchReform"
        data = {
            "gender": gender,
            "userGender": user_gender,
            "cardNo": card_no,
            "skuId": sku_id,
            "optionalItemSkuIds": optional_item_sku_ids
        }
        return self._post(url, data, need_auth=True)

    # ============== Step 7b-3: 下单前校验-婚姻状态 ==============
    def check_married_status(
        self,
        pkg_id: int,
        item_list: List[str],
        sex: int,
        married: int,
        station_id: str,
        reserve_id: str = ""
    ) -> ApiResponse:
        """
        Step 7b-3: 下单前校验-验证婚姻状态（需要登录）
        
        Args:
            pkg_id: 套餐ID
            item_list: 检查项目ID列表
            sex: 性别（1=男, 2=女）
            married: 婚姻状态（0=未婚, 1=已婚）
            station_id: 医院ID
            reserve_id: 预约ID
        
        Returns:
            ApiResponse: 校验结果
                result: true表示婚姻状态匹配，可以继续下单
        """
        url = f"{BASE_URL_WX}/wx/api/examination/addition/itemMarriedCheck"
        data = {
            "pkgId": pkg_id,
            "itemList": item_list,
            "sex": sex,
            "married": married,
            "reserveId": reserve_id,
            "stationId": station_id
        }
        return self._post(url, data, need_auth=True)

    # ============== Step 7c: 生成预约单 ==============
    def create_reservation(
        self,
        station_id: str,
        reserve_day: int,
        sku_ids: List[int],
        user_id: str,
        real_name: str,
        card_no: str,
        gender: int,
        married: int,
        age: int,
        mobile: str = "",
        branch_id: Union[int, str] = 0,
        birthday: str = "",
        prohibition_crowd: int = 0,
        department: str = "",
        job_number: str = "",
        company_name: str = "",
        is_group: str = "0",
        reserve_type: int = 0,
        reserve_from: int = 0,
        self_addition_sku_ids: List = None,
        user_card_id: str = "",
        trade_type: str = "200",
        exampackage_pkg_id: Any = None,
        selfie_image: str = "",
        patient_id: str = "",
        check_time: str = ""
    ) -> ApiResponse:
        """
        Step 7c: 生成预约单（需要登录）
        
        Args:
            station_id: 医院ID
            reserve_day: 预约日期时间戳（毫秒，秒级时间戳需×1000）
            sku_ids: SKU ID列表
            user_id: 用户ID（helianhealthcheck_uid）
            real_name: 姓名
            card_no: 身份证号
            gender: 性别（1=男, 2=女）
            married: 婚姻状态（0=未婚, 1=已婚）
            age: 年龄
            mobile: 手机号
            branch_id: 院区ID，无分院区传0
            birthday: 生日
            prohibition_crowd: 禁忌人群，默认0
            department: 部门
            job_number: 工号
            company_name: 公司名称
            is_group: 是否团体，固定"0"
            reserve_type: 预约类型
            reserve_from: 预约来源
            self_addition_sku_ids: 自选加项SKU ID列表
            user_card_id: 用户卡ID
            trade_type: 交易类型，固定"200"
            exampackage_pkg_id: 体检包ID
            selfie_image: 自拍照
            patient_id: 患者ID
            check_time: 时间段（如"05:00-05:30"）
        
        Returns:
            ApiResponse: 预约结果
                result: 预约单号 (reservationId)
        """
        url = f"{BASE_URL_WX}/app/my/reserve/userPersonalReserve"
        # 确保时间戳是毫秒级
        if reserve_day < 10000000000:
            reserve_day = reserve_day * 1000
        data = {
            "branchId": branch_id,
            "reserveDay": reserve_day,
            "married": married,
            "cardNo": card_no,
            "age": age,
            "birthday": birthday,
            "gender": gender,
            "realName": real_name,
            "prohibitionCrowd": prohibition_crowd,
            "department": department,
            "jobNumber": job_number,
            "companyName": company_name,
            "isGroup": is_group,
            "mobile": mobile,
            "reserveType": reserve_type,
            "reserveFrom": reserve_from,
            "skuIds": sku_ids,
            "selfAdditionSkuIds": self_addition_sku_ids or [],
            "userId": user_id,
            "stationId": station_id,
            "userCardId": user_card_id,
            "tradeType": trade_type,
            "exampackagePkgId": exampackage_pkg_id,
            "selfieImage": selfie_image,
            "patientId": patient_id,
            "checkTime": check_time
        }
        return self._post(url, data, need_auth=True)

    # ============== Step 7d: 生成订单 ==============
    def create_order(
        self,
        sku_id: int,
        pay_amount: str,
        reservation_id: int,
        trade_channel: int = 68,
        user_coupon_id: str = "",
        ecard_nos: List = None,
        ecard_select_type: str = "-1",
        trade_type: str = "200",
        pay_mode: int = 0,
        mch_id: str = "",
        trade_os: int = 1,
        trade_source: str = "",
        insurance_dto: Any = None,
        hm_service_dto: List = None,
        app_id: str = "",
        open_id: str = "",
        exampackage_pkg_id: Any = None
    ) -> ApiResponse:
        """
        Step 7d: 生成订单（需要登录）
        
        Args:
            sku_id: SKU ID（来自套餐详情的skuId）
            pay_amount: 支付金额
            reservation_id: 预约单号（来自生成预约单的返回）
            trade_channel: 交易渠道，默认68
            user_coupon_id: 用户优惠券ID
            ecard_nos: 电子卡号列表
            ecard_select_type: 电子卡选择类型
            trade_type: 交易类型，固定"200"
            pay_mode: 支付方式
            mch_id: 商户ID
            trade_os: 交易系统
            trade_source: 交易来源
            insurance_dto: 保险信息
            hm_service_dto: 健康管理服务
            app_id: 应用ID
            open_id: OpenID
            exampackage_pkg_id: 体检包ID
        
        Returns:
            ApiResponse: 订单结果
                result.tradeId: 订单号
                result.tradeResult: 交易结果（"CREATE_TRADE_SUCCESS"表示成功）
                result.needPay: 是否需要支付（1=需要）
        """
        url = f"{BASE_URL_WX}/app/api/market/trade/create"
        
        # 构建ext字段
        ext = {
            "groupUserCardId": "",
            "tradeGroupCardBindType": "0",
            "hostTradeId": "",
            "examinationReservePo": {
                "reserveId": reservation_id,
                "receiverProvince": "",
                "receiverCity": "",
                "receiverDistrict": "",
                "receiverAddress": "",
                "receiverZip": "",
                "nationality": "",
                "ethnic": "",
                "reportMailMobile": "",
                "reportMailAddress": "",
                "needReportMail": 0
            },
            "selfSelectedItems": [],
            "exampackagePkgId": exampackage_pkg_id
        }
        
        data = {
            "itemDpList": [{"goodsSkuId": sku_id, "count": 1}],
            "packDpList": [],
            "payAmount": pay_amount,
            "tradeChannel": trade_channel,
            "ext": json.dumps(ext, ensure_ascii=False),
            "userCouponId": user_coupon_id,
            "ecardNos": ecard_nos or [],
            "ecardSelectType": ecard_select_type,
            "tradeType": trade_type,
            "payMode": pay_mode,
            "mchId": mch_id,
            "tradeOS": trade_os,
            "tradeSource": trade_source,
            "insuranceDTO": insurance_dto,
            "hmServiceDTO": hm_service_dto or [],
            "appId": app_id,
            "openId": open_id
        }
        return self._post(url, data, need_auth=True)


# ============== 工具函数 ==============
def calculate_age_from_id_card(id_card: str) -> int:
    """
    根据身份证号计算年龄
    
    Args:
        id_card: 18位身份证号
    
    Returns:
        int: 年龄
    """
    if len(id_card) != 18:
        return 0
    
    try:
        birth_year = int(id_card[6:10])
        birth_month = int(id_card[10:12])
        birth_day = int(id_card[12:14])
        
        from datetime import datetime
        today = datetime.now()
        age = today.year - birth_year
        
        # 如果生日还没过，年龄减1
        if (today.month, today.day) < (birth_month, birth_day):
            age -= 1
        
        return age
    except:
        return 0


def get_gender_from_id_card(id_card: str) -> int:
    """
    根据身份证号获取性别
    
    Args:
        id_card: 18位身份证号
    
    Returns:
        int: 1=男, 2=女
    """
    if len(id_card) != 18:
        return 0
    
    try:
        # 身份证第17位奇数为男，偶数为女
        return 1 if int(id_card[16]) % 2 == 1 else 2
    except:
        return 0


def parse_exam_item_ids(exam_item_new_list: str) -> List[str]:
    """
    从套餐详情的examItemNewList解析检查项目ID列表
    
    Args:
        exam_item_new_list: examItemNewList的JSON字符串
    
    Returns:
        List[str]: examFeeItemID列表
    """
    try:
        items = json.loads(exam_item_new_list)
        result = []
        for group in items:
            if "itemDos" in group:
                for item in group["itemDos"]:
                    if "examFeeItemID" in item:
                        result.append(item["examFeeItemID"])
        return result
    except:
        return []


def parse_exam_item_names(exam_item_new_list: str) -> List[str]:
    """
    从套餐详情的examItemNewList解析检查项目名称列表
    
    Args:
        exam_item_new_list: examItemNewList的JSON字符串
    
    Returns:
        List[str]: 检查项目名称列表
    """
    try:
        items = json.loads(exam_item_new_list)
        result = []
        for group in items:
            if "itemDos" in group:
                for item in group["itemDos"]:
                    item_name = item.get("examFeeItemName", "")
                    if item_name:
                        result.append(item_name)
        return result
    except:
        return []


def parse_disease_names(disease_json: str) -> List[str]:
    """
    从套餐详情的diseaseJson解析可筛查疾病名称列表
    
    Args:
        disease_json: diseaseJson的JSON字符串
    
    Returns:
        List[str]: 可筛查疾病名称列表
    """
    try:
        diseases = json.loads(disease_json)
        result = []
        for disease in diseases:
            disease_name = disease.get("diseaseName", "")
            if disease_name:
                result.append(disease_name)
        return result
    except:
        return []


# ============== 使用示例 ==============
if __name__ == "__main__":
    # 创建服务实例
    service = HealthCheckService()
    
    # Step 1: 查询医院列表
    print("=== Step 1: 查询医院列表 ===")
    result = service.get_hospital_list()
    if result.success:
        hospitals = result.result.get("list", [])
        print(f"找到 {len(hospitals)} 家医院")
        for h in hospitals[:3]:
            print(f"  - {h.get('stationName')} ({h.get('stationId')})")
    
    # Step 2: 查询套餐列表
    print("\n=== Step 2: 查询套餐列表 ===")
    result = service.get_package_list("HL99997")
    if result.success:
        packages = result.result.get("list", [])
        print(f"找到 {len(packages)} 个套餐")
        for p in packages[:3]:
            print(f"  - {p.get('goodsName')} (¥{p.get('salePrice')})")
