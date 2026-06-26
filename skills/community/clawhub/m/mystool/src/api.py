"""
米游社 API 封装
参考: https://github.com/Ljzd-PRO/nonebot-plugin-mystool
"""

import asyncio
import hashlib
import json
import random
import string
import time
from typing import Any, Dict, List, Optional, Tuple

import httpx

# ── 常量 ──────────────────────────────────────────────────────────────────────

APP_VERSION = "2.99.1"
CLIENT_TYPE = "5"
# Salt 值（来自 MihoyoBBSTools）
SALT_IOS = "IZPgfb0dRPtBeLuFkdDznSmmkB5W5EXc"
SALT_PROD = "6s25p5ox5y14umn1p61aqyyvbvvl3lrt"
SALT_WEB = "DlOUwIupfU6YespEUWDJmXtutuXV6owG"  # 网页端
SALT_X6 = "t0qEgfub6cvueAPgR5m9aQWWVciEer7v"  # 点赞/分享专用
SALT_APP = "b0EofkfMKq2saWV9fwux18J5vzcFTlex"  # App 端

# 米游社 verify_key
BBS_VERIFY_KEY = "bll8iq97cem8"

UA_MOBILE = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.44.1"
)

# 游戏签到 API（仅国服）
SIGN_APIS = {
    "genshin": {
        "name": "原神",
        "game_id": "hk4e_cn",
        "act_id": "e202311201442471",
        "cn": {
            "act_id": "e202311201442471",
            "url": "https://api-takumi.mihoyo.com/event/luna/sign",
            "info_url": "https://api-takumi.mihoyo.com/event/luna/info",
            "referer": "https://webstatic.mihoyo.com/",
        },
        "signgame": "hk4e",
    },
    "starrail": {
        "name": "崩坏：星穹铁道",
        "game_id": "hkrpg_cn",
        "act_id": "e202304121516551",
        "cn": {
            "act_id": "e202304121516551",
            "url": "https://api-takumi.mihoyo.com/event/luna/hkrpg/sign",
            "info_url": "https://api-takumi.mihoyo.com/event/luna/hkrpg/info",
            "referer": "https://webstatic.mihoyo.com/",
        },
        "signgame": "hkrpg",
    },
    "honkai3": {
        "name": "崩坏3",
        "game_id": "bh3_cn",
        "act_id": "e202306201626331",
        "cn": {
            "act_id": "e202306201626331",
            "url": "https://api-takumi.mihoyo.com/event/luna/bh3/sign",
            "info_url": "https://api-takumi.mihoyo.com/event/luna/bh3/info",
            "referer": "https://webstatic.mihoyo.com/",
        },
        "signgame": "bh3",
    },
    "honkai2": {
        "name": "崩坏学园2",
        "game_id": "bh2_cn",
        "act_id": "e202203291431091",
        "cn": {
            "act_id": "e202203291431091",
            "url": "https://api-takumi.mihoyo.com/event/luna/bh2/sign",
            "info_url": "https://api-takumi.mihoyo.com/event/luna/bh2/info",
            "referer": "https://webstatic.mihoyo.com/",
        },
        "signgame": "bh2",
    },
    "tearsofthemis": {
        "name": "未定事件簿",
        "game_id": "nxx_cn",
        "act_id": "e202202251749321",
        "cn": {
            "act_id": "e202202251749321",
            "url": "https://api-takumi.mihoyo.com/event/luna/nxx/sign",
            "info_url": "https://api-takumi.mihoyo.com/event/luna/nxx/info",
            "referer": "https://webstatic.mihoyo.com/",
        },
        "signgame": "nxx",
    },
    "zzz": {
        "name": "绝区零",
        "game_id": "nap_cn",
        "act_id": "e202406242138391",
        "cn": {
            "act_id": "e202406242138391",
            "url": "https://act-nap-api.mihoyo.com/event/luna/zzz/sign",
            "info_url": "https://act-nap-api.mihoyo.com/event/luna/zzz/info",
            "referer": "https://webstatic.mihoyo.com/",
        },
        "signgame": "zzz",
    },
}

# 米游币任务 API
URL_BBS_TASKS = "https://bbs-api.miyoushe.com/apihub/wapi/getUserMissionsState"
URL_BBS_SIGN = "https://bbs-api.miyoushe.com/apihub/app/api/signIn"
URL_BBS_LIST = "https://bbs-api.miyoushe.com/post/api/getForumPostList?forum_id={forum_id}&is_good=false&is_hot=false&page_size=20&sort_type=1"
URL_BBS_VIEW = "https://bbs-api.miyoushe.com/post/api/getPostFull?post_id={post_id}"
URL_BBS_LIKE = "https://bbs-api.miyoushe.com/apihub/sapi/upvotePost"
URL_BBS_SHARE = "https://bbs-api.miyoushe.com/apihub/api/getShareConf?entity_id={post_id}&entity_type=1"

# 便笺 API
URL_GENSHIN_NOTE = "https://api-takumi-record.mihoyo.com/game_record/app/genshin/api/dailyNote"
URL_STARRAIL_NOTE = "https://api-takumi-record.mihoyo.com/game_record/app/hkrpg/api/note"

# 游戏账号 API
URL_GAME_RECORD = "https://api-takumi-record.mihoyo.com/game_record/card/wapi/getGameRecordCard?uid={uid}"
URL_ACCOUNT_BY_GAME = "https://api-takumi.mihoyo.com/binding/api/getUserGameRolesByCookie?game_biz={game_biz}"

# 商品 API
URL_GOOD_LIST = "https://api-takumi.mihoyo.com/mall/v1/web/goods/list?app_id=1&point_sn=myb&page_size=20&page={page}&game={game}"
URL_EXCHANGE = "https://api-takumi.miyoushe.com/mall/v1/web/goods/exchange"

# 米游币余额
URL_MYB = "https://api-takumi.mihoyo.com/common/homutreasure/v1/web/user/point?app_id=1&point_sn=myb"

# 地址列表
URL_ADDRESS_LIST = "https://api-takumi.mihoyo.com/account/address/list"

# 论坛 ID（用于米游币任务）
FORUM_IDS = {
    "genshin": 26,
    "starrail": 52,
    "honkai3": 1,
    "zzz": 57,
}


# ── DS 签名生成 ────────────────────────────────────────────────────────────────

def generate_ds(salt: str = SALT_IOS, body: str = "", query: str = "") -> str:
    """
    生成米游社请求所需的 DS 签名
    
    :param salt: 签名 salt
    :param body: 请求体 JSON 字符串
    :param query: URL 查询参数字符串
    :return: DS 签名字符串
    """
    t = str(int(time.time()))
    # X6 salt 使用数字随机数，其他使用字母数字
    if salt == SALT_X6:
        r = str(random.randint(100001, 200000))
        h = hashlib.md5(f"salt={salt}&t={t}&r={r}&b={body}&q={query}".encode()).hexdigest()
    elif salt == SALT_APP:
        # APP salt 使用简单格式（无 body/query）
        r = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        h = hashlib.md5(f"salt={salt}&t={t}&r={r}".encode()).hexdigest()
    else:
        r = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
        h = hashlib.md5(f"salt={salt}&t={t}&r={r}&b={body}&q={query}".encode()).hexdigest()
    return f"{t},{r},{h}"


def generate_device_id() -> str:
    """生成随机设备 ID"""
    import uuid
    return str(uuid.uuid4()).upper()


# ── 通用请求头 ─────────────────────────────────────────────────────────────────

def get_base_headers(cookies: Dict[str, str]) -> Dict[str, str]:
    return {
        "User-Agent": UA_MOBILE,
        "Referer": "https://webstatic.mihoyo.com/",
        "Origin": "https://webstatic.mihoyo.com",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "x-rpc-app_version": APP_VERSION,
        "x-rpc-client_type": CLIENT_TYPE,
        "x-rpc-device_id": generate_device_id(),
    }


# ── 账号信息 ───────────────────────────────────────────────────────────────────

async def get_game_records(cookies: Dict[str, str], uid: str) -> Tuple[bool, Optional[List[Dict]]]:
    """获取用户绑定的游戏账号列表"""
    headers = get_base_headers(cookies)
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                URL_GAME_RECORD.format(uid=uid),
                headers=headers,
                cookies=cookies,
                timeout=15,
            )
        data = res.json()
        if data.get("retcode") == 0:
            return True, data["data"]["list"]
        return False, None
    except Exception:
        return False, None


async def get_account_list_by_game(cookies: Dict[str, str], game_biz: str) -> List[Dict[str, str]]:
    """
    按游戏获取账号列表（参考 MihoyoBBSTools/account.py）
    :param cookies: 米游社 Cookie
    :param game_biz: 游戏业务标识 (hk4e_cn/hkrpg_cn/bh3_cn/bh2_cn/nxx_cn/nap_cn)
    :return: 账号列表 [{"nickname": str, "game_uid": str, "region": str}, ...]
    """
    headers = get_base_headers(cookies)
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                URL_ACCOUNT_BY_GAME.format(game_biz=game_biz),
                headers=headers,
                cookies=cookies,
                timeout=15,
            )
        data = res.json()
        if data.get("retcode") == 0:
            accounts = []
            for item in data["data"].get("list", []):
                accounts.append({
                    "nickname": item.get("nickname", ""),
                    "game_uid": item.get("game_uid", ""),
                    "region": item.get("region", ""),
                })
            return accounts
        return []
    except Exception:
        return []


async def get_myb_balance(cookies: Dict[str, str]) -> Tuple[bool, Optional[int]]:
    """获取米游币余额"""
    headers = get_base_headers(cookies)
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(URL_MYB, headers=headers, cookies=cookies, timeout=15)
        data = res.json()
        if data.get("retcode") == 0:
            return True, int(data["data"]["points"])
        return False, None
    except Exception:
        return False, None



# ── 米游币每日任务（忠实移植 MihoyoBBSTools/mihoyobbs.py）────────────────────────

# 论坛列表（对应 MihoyoBBSTools setting.mihoyobbs_List）
BBS_LIST = {
    "genshin": {"id": "2", "forumId": "26", "name": "原神"},
    "starrail": {"id": "6", "forumId": "52", "name": "崩坏：星穹铁道"},
    "honkai3": {"id": "1", "forumId": "1", "name": "崩坏3"},
    "honkai2": {"id": "3", "forumId": "30", "name": "崩坏学园2"},
    "tearsofthemis": {"id": "4", "forumId": "37", "name": "未定事件簿"},
    "zzz": {"id": "8", "forumId": "57", "name": "绝区零"},
}

# 任务 ID 映射（对应 MihoyoBBSTools get_tasks_list）
TASK_IDS = {
    58: {"attr": "sign", "done": "is_get_award"},
    59: {"attr": "read", "done": "is_get_award", "num_attr": "read_num"},
    60: {"attr": "like", "done": "is_get_award", "num_attr": "like_num"},
    61: {"attr": "share", "done": "is_get_award"},
}


def _get_ds(salt: str = SALT_APP) -> str:
    """生成 DS 签名（对应 MihoyoBBSTools get_ds(web=False)）"""
    t = str(int(time.time()))
    r = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    h = hashlib.md5(f"salt={salt}&t={t}&r={r}".encode()).hexdigest()
    return f"{t},{r},{h}"


def _get_ds2(query: str = "", body: str = "") -> str:
    """生成 DS 签名（对应 MihoyoBBSTools get_ds2）"""
    t = str(int(time.time()))
    r = str(random.randint(100001, 200000))
    h = hashlib.md5(f"salt={SALT_X6}&t={t}&r={r}&b={body}&q={query}".encode()).hexdigest()
    return f"{t},{r},{h}"


def _get_stoken_cookie(cookies: Dict[str, str]) -> str:
    """构建 stoken cookie 字符串"""
    stuid = cookies.get("stuid") or cookies.get("account_id", "")
    stoken = cookies.get("stoken", "")
    mid = cookies.get("mid", "")
    ck = f"stuid={stuid};stoken={stoken}"
    if mid:
        ck += f";mid={mid}"
    return ck


def _get_device_id(cookie_str: str) -> str:
    """用 cookie 通过 uuid v3 生成设备 ID（对应 MihoyoBBSTools get_device_id）"""
    import uuid
    return str(uuid.uuid3(uuid.NAMESPACE_URL, cookie_str))


class _Mihoyobbs:
    """忠实移植 MihoyoBBSTools/Mihoyobbs 类为异步版本"""

    def __init__(self, cookies: Dict[str, str], game: str = "genshin"):
        self.cookies = cookies
        self.bbs_config = {
            "checkin": True, "read": True, "like": True, "share": True, "cancel_like": False,
        }
        self.bbs_list = [BBS_LIST.get(game, BBS_LIST["genshin"])]

        stoken_cookie = _get_stoken_cookie(cookies)
        device_id = _get_device_id(stoken_cookie)

        self.headers = {
            "DS": _get_ds(SALT_APP),
            "cookie": stoken_cookie,
            "x-rpc-client_type": "2",
            "x-rpc-app_version": APP_VERSION,
            "x-rpc-sys_version": "12",
            "x-rpc-channel": "miyousheluodi",
            "x-rpc-device_id": device_id,
            "x-rpc-device_name": "Unknown",
            "x-rpc-device_model": "Unknown",
            "x-rpc-h265_supported": "1",
            "Referer": "https://app.mihoyo.com",
            "x-rpc-verify_key": BBS_VERIFY_KEY,
            "x-rpc-csm_source": "discussion",
            "Content-Type": "application/json; charset=UTF-8",
            "Host": "bbs-api.miyoushe.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/4.9.3",
        }

        # 任务列表查询 headers（web 端）
        account_cookie = ""
        for k in ["account_id", "cookie_token", "stuid", "stoken"]:
            if cookies.get(k):
                account_cookie += f"{k}={cookies[k]};"
        self.task_header = {
            "Accept": "application/json, text/plain, */*",
            "Origin": "https://webstatic.mihoyo.com",
            "User-Agent": (
                f"Mozilla/5.0 (Linux; Android 12; Unspecified Device) AppleWebKit/537.36 "
                f"(KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.129 Mobile Safari/537.36 "
                f"miHoYoBBS/{APP_VERSION}"
            ),
            "Referer": "https://webstatic.mihoyo.com",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,en-US;q=0.8",
            "X-Requested-With": "com.mihoyo.hyperion",
            "Cookie": account_cookie,
        }

        self.today_get_coins = 0
        self.today_have_get_coins = 0
        self.have_coins = 0
        self.task_do = {
            "sign": False, "read": False, "read_num": 3,
            "like": False, "like_num": 5, "share": False,
        }
        self.posts_list: List[list] = []

    async def _get_tasks_list(self):
        """获取任务列表"""
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(
                    URL_BBS_TASKS,
                    params={"point_sn": "myb"},
                    headers=self.task_header,
                    timeout=15,
                )
            data = res.json()
            if "err" in data.get("message", "") or data.get("retcode") == -100:
                return
            self.today_get_coins = data["data"]["can_get_points"]
            self.today_have_get_coins = data["data"]["already_received_points"]
            self.have_coins = data["data"]["total_points"]
            if self.today_get_coins == 0:
                self.task_do["sign"] = True
                self.task_do["read"] = True
                self.task_do["like"] = True
                self.task_do["share"] = True
                return
            missions = data["data"].get("states", [])
            for task_id, do_info in TASK_IDS.items():
                mission = next((x for x in missions if x["mission_id"] == task_id), None)
                if mission is None:
                    continue
                if mission[do_info["done"]]:
                    self.task_do[do_info["attr"]] = True
                elif do_info.get("num_attr"):
                    self.task_do[do_info["num_attr"]] -= mission["happened_times"]
        except Exception:
            pass

    async def _get_posts_list(self):
        """获取帖子列表"""
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(
                    URL_BBS_LIST.format(forum_id=self.bbs_list[0]["forumId"]),
                    headers=self.headers,
                    timeout=15,
                )
            data = res.json()["data"]["list"]
            max_num = max(self.task_do["read_num"], self.task_do["like_num"])
            self.posts_list = []
            while len(self.posts_list) < max_num:
                post = random.choice(data)
                if post["post"]["post_id"] not in [x[0] for x in self.posts_list]:
                    self.posts_list.append([post["post"]["post_id"], post["post"]["subject"]])
        except Exception:
            pass

    async def _signing(self):
        """论坛打卡"""
        if self.task_do["sign"]:
            return
        for forum in self.bbs_list:
            try:
                post_data = json.dumps({"gids": forum["id"]})
                h = self.headers.copy()
                h["DS"] = _get_ds2("", post_data)
                async with httpx.AsyncClient() as client:
                    res = await client.post(
                        URL_BBS_SIGN, data=post_data, headers=h, timeout=15,
                    )
                data = res.json()
                if data.get("retcode") in (0, -5003):
                    self.task_do["sign"] = True
            except Exception:
                pass
            await asyncio.sleep(random.randint(2, 4))

    async def _read_post(self, post_info: list):
        """浏览帖子"""
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(
                    URL_BBS_VIEW.format(post_id=post_info[0]),
                    headers=self.headers, timeout=15,
                )
            return res.json().get("message") == "OK"
        except Exception:
            return False

    async def _like_post(self, post_info: list) -> bool:
        """点赞帖子"""
        try:
            h = self.headers.copy()
            h["DS"] = _get_ds(SALT_APP)
            async with httpx.AsyncClient() as client:
                res = await client.post(
                    URL_BBS_LIKE, headers=h,
                    json={"post_id": post_info[0], "is_cancel": False},
                    timeout=15,
                )
            return res.json().get("message") == "OK"
        except Exception:
            return False

    async def _share_post(self, post_info: list) -> bool:
        """分享帖子（重试 3 次）"""
        for _ in range(3):
            try:
                h = self.headers.copy()
                h["DS"] = _get_ds(SALT_APP)
                async with httpx.AsyncClient() as client:
                    res = await client.get(
                        URL_BBS_SHARE.format(post_id=post_info[0]),
                        headers=h, timeout=15,
                    )
                if res.json().get("message") == "OK":
                    return True
            except Exception:
                pass
            await asyncio.sleep(random.randint(2, 4))
        return False

    async def _post_task(self):
        """执行帖子相关任务"""
        if self.task_do["read"] and self.task_do["like"] and self.task_do["share"]:
            return
        for post in self.posts_list:
            if self.bbs_config["read"] and not self.task_do["read"] and self.task_do["read_num"] > 0:
                await self._read_post(post)
                self.task_do["read_num"] -= 1
                await asyncio.sleep(random.randint(3, 8))
            if self.bbs_config["like"] and not self.task_do["like"] and self.task_do["like_num"] > 0:
                await self._like_post(post)
                self.task_do["like_num"] -= 1
                await asyncio.sleep(random.randint(3, 8))
            if self.bbs_config["share"] and not self.task_do["share"]:
                if await self._share_post(post):
                    self.task_do["share"] = True
                await asyncio.sleep(random.randint(3, 8))

    async def run(self) -> Dict[str, Any]:
        """执行全部米游币任务"""
        await self._get_tasks_list()
        if self.task_do["sign"] and self.task_do["read"] and self.task_do["like"] and self.task_do["share"]:
            return {
                "sign": {"done": 1, "total": 1, "success": True},
                "view": {"done": 3, "total": 3, "success": True},
                "like": {"done": 5, "total": 5, "success": True},
                "share": {"done": 1, "total": 1, "success": True},
                "coins": {"got": self.today_have_get_coins, "remaining": 0, "total": self.have_coins},
            }
        await self._get_posts_list()
        if not self.posts_list:
            return {
                "sign": {"done": int(self.task_do["sign"]), "total": 1, "success": self.task_do["sign"]},
                "view": {"done": 3 - self.task_do["read_num"], "total": 3, "success": self.task_do["read"]},
                "like": {"done": 5 - self.task_do["like_num"], "total": 5, "success": self.task_do["like"]},
                "share": {"done": int(self.task_do["share"]), "total": 1, "success": self.task_do["share"]},
                "error": "获取帖子列表失败",
            }
        for i in range(2):
            if i > 0:
                await asyncio.sleep(random.randint(3, 8))
                await self._get_posts_list()
            if self.bbs_config["checkin"]:
                await self._signing()
            await self._post_task()
            await self._get_tasks_list()
            if self.task_do["sign"] and self.task_do["read"] and self.task_do["like"] and self.task_do["share"]:
                break
        return {
            "sign": {"done": int(self.task_do["sign"]), "total": 1, "success": self.task_do["sign"]},
            "view": {"done": 3 - self.task_do["read_num"], "total": 3, "success": self.task_do["read"]},
            "like": {"done": 5 - self.task_do["like_num"], "total": 5, "success": self.task_do["like"]},
            "share": {"done": int(self.task_do["share"]), "total": 1, "success": self.task_do["share"]},
            "coins": {"got": self.today_have_get_coins, "remaining": self.today_get_coins, "total": self.have_coins},
        }


async def do_bbs_tasks(cookies: Dict[str, str], game: str = "genshin") -> Dict[str, Any]:
    """执行米游币每日任务（忠实移植 MihoyoBBSTools/mihoyobbs.py）"""
    bbs = _Mihoyobbs(cookies, game)
    return await bbs.run()


# ── 游戏签到（基于 MihoyoBBSTools/gamecheckin.py 改写）───────────────────────────

# 游戏签到配置（对应 MihoyoBBSTools 的 game_id, act_id 等）
GAME_CHECKIN_CONFIG = {
    "genshin": {
        "game_id": "hk4e_cn",
        "name": "原神",
        "act_id": "e202311201442471",
        "signgame": "hk4e",
        "player_name": "旅行者",
        # 使用默认 API
    },
    "starrail": {
        "game_id": "hkrpg_cn",
        "name": "崩坏：星穹铁道",
        "act_id": "e202304121516551",
        "signgame": "hkrpg",
        "player_name": "开拓者",
    },
    "honkai3": {
        "game_id": "bh3_cn",
        "name": "崩坏3",
        "act_id": "e202306201626331",
        "player_name": "舰长",
    },
    "honkai2": {
        "game_id": "bh2_cn",
        "name": "崩坏学园2",
        "act_id": "e202203291431091",
        "player_name": "玩家",
    },
    "tearsofthemis": {
        "game_id": "nxx_cn",
        "name": "未定事件簿",
        "act_id": "e202202251749321",
        "player_name": "律师",
    },
    "zzz": {
        "game_id": "nap_cn",
        "name": "绝区零",
        "act_id": "e202406242138391",
        "signgame": "zzz",
        "player_name": "绳匠",
        # 绝区零使用独立 API
        "use_zzz_api": True,
    },
}


def _get_game_checkin_headers(cookies: Dict[str, str], game: str) -> Dict[str, str]:
    """生成游戏签到 headers（对应 MihoyoBBSTools 的 set_headers）"""
    device_id = generate_device_id()
    
    # 构建 cookie 字符串
    cookie_parts = []
    for key in ["account_id", "cookie_token", "ltoken", "ltuid", "mid", "stoken", "stuid"]:
        if cookies.get(key):
            cookie_parts.append(f"{key}={cookies[key]}")
    cookie_str = ";".join(cookie_parts)
    
    headers = {
        "DS": _get_ds(salt=SALT_WEB),
        "Referer": "https://act.mihoyo.com/",
        "Cookie": cookie_str,
        "x-rpc-device_id": device_id,
        "User-Agent": f"Mozilla/5.0 (Linux; Android 12; Unspecified Device) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/103.0.5060.129 Mobile Safari/537.36 miHoYoBBS/{APP_VERSION}",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "zh-CN,en-US;q=0.8",
        "x-rpc-app_version": APP_VERSION,
        "x-rpc-client_type": "5",
        "Content-Type": "application/json;charset=utf-8",
    }
    
    # 特殊处理
    cfg = GAME_CHECKIN_CONFIG.get(game, {})
    if game == "genshin":
        headers["Origin"] = "https://act.mihoyo.com"
        headers["x-rpc-signgame"] = "hk4e"
    elif game == "zzz":
        headers["Origin"] = "https://act.mihoyo.com"
        headers["X-Rpc-Signgame"] = "zzz"
    
    return headers


async def game_sign(cookies: Dict[str, str], game: str, region: str = "cn_gf01", uid: str = "") -> Tuple[bool, str]:
    """
    执行游戏签到（基于 MihoyoBBSTools 实现）
    :param cookies: 米游社 Cookie
    :param game: 游戏标识
    :param region: 服务器区域
    :param uid: 游戏 UID
    :return: (是否成功, 消息)
    """
    cfg = GAME_CHECKIN_CONFIG.get(game)
    if not cfg:
        return False, f"不支持的游戏: {game}"
    
    game_name = cfg["name"]
    act_id = cfg["act_id"]
    
    # 判断 API 端点
    if cfg.get("use_zzz_api"):
        # 绝区零使用独立 API
        sign_url = "https://act-nap-api.mihoyo.com/event/luna/zzz/sign"
        info_url = "https://act-nap-api.mihoyo.com/event/luna/zzz/info"
    elif game == "starrail":
        sign_url = "https://api-takumi.mihoyo.com/event/luna/hkrpg/sign"
        info_url = "https://api-takumi.mihoyo.com/event/luna/hkrpg/info"
    elif game == "honkai3":
        sign_url = "https://api-takumi.mihoyo.com/event/luna/bh3/sign"
        info_url = "https://api-takumi.mihoyo.com/event/luna/bh3/info"
    elif game == "honkai2":
        sign_url = "https://api-takumi.mihoyo.com/event/luna/bh2/sign"
        info_url = "https://api-takumi.mihoyo.com/event/luna/bh2/info"
    elif game == "tearsofthemis":
        sign_url = "https://api-takumi.mihoyo.com/event/luna/nxx/sign"
        info_url = "https://api-takumi.mihoyo.com/event/luna/nxx/info"
    else:
        # 原神
        sign_url = "https://api-takumi.mihoyo.com/event/luna/sign"
        info_url = "https://api-takumi.mihoyo.com/event/luna/info"
    
    headers = _get_game_checkin_headers(cookies, game)
    
    # 1. 查询签到状态
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                info_url,
                params={"act_id": act_id, "region": region, "uid": uid},
                headers=headers,
                timeout=15,
            )
        data = res.json()
        if data.get("retcode") == 0:
            if data["data"].get("is_sign"):
                return True, f"{game_name} 今日已签到"
            # 首次绑定检查
            if data["data"].get("first_bind"):
                return False, f"{game_name} 首次绑定，请先手动签到一次"
    except Exception:
        pass
    
    await asyncio.sleep(random.randint(2, 8))
    
    # 2. 执行签到
    try:
        # 重新生成 DS
        headers["DS"] = _get_ds(salt=SALT_WEB)
        
        async with httpx.AsyncClient() as client:
            res = await client.post(
                sign_url,
                headers=headers,
                json={"act_id": act_id, "region": region, "uid": uid},
                timeout=15,
            )
        data = res.json()
        retcode = data.get("retcode", -1)
        
        if retcode == 0 and data.get("data", {}).get("success") == 0:
            return True, f"{game_name} 签到成功 🎉"
        elif retcode == -5003:
            return True, f"{game_name} 今日已签到"
        elif retcode == 1034:
            return False, f"{game_name} 触发验证码，请手动签到"
        else:
            return False, f"{game_name} 签到失败: {data.get('message', '未知错误')}"
    except Exception as e:
        return False, f"{game_name} 签到请求失败: {e}"


# ── 实时便笺 ───────────────────────────────────────────────────────────────────

async def get_genshin_note(cookies: Dict[str, str], uid: str, region: str = "cn_gf01") -> Tuple[bool, Optional[Dict]]:
    """获取原神实时便笺（树脂、洞天、探索派遣等）"""
    headers = get_base_headers(cookies)
    headers["DS"] = generate_ds(
        salt=SALT_PROD,
        query=f"role_id={uid}&server={region}",
    )
    headers["x-rpc-tool_version"] = "v4.2.2-ys"
    headers["x-rpc-page"] = "v4.2.2-ys_#/ys/daily"
    headers["X-Requested-With"] = "com.mihoyo.hyperion"

    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                URL_GENSHIN_NOTE,
                params={"role_id": uid, "server": region},
                headers=headers,
                cookies=cookies,
                timeout=15,
            )
        data = res.json()
        if data.get("retcode") == 0:
            return True, data["data"]
        return False, None
    except Exception:
        return False, None


async def get_starrail_note(cookies: Dict[str, str], uid: str, region: str = "prod_gf_cn") -> Tuple[bool, Optional[Dict]]:
    """获取星穹铁道实时便笺（开拓力、每日实训等）"""
    headers = get_base_headers(cookies)
    headers["DS"] = generate_ds(
        salt=SALT_PROD,
        query=f"role_id={uid}&server={region}",
    )

    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                URL_STARRAIL_NOTE,
                params={"role_id": uid, "server": region},
                headers=headers,
                cookies=cookies,
                timeout=15,
            )
        data = res.json()
        if data.get("retcode") == 0:
            return True, data["data"]
        return False, None
    except Exception:
        return False, None


# ── 商品兑换 ───────────────────────────────────────────────────────────────────

async def get_good_list(game: str = "", page: int = 1) -> Tuple[bool, Optional[List[Dict]]]:
    """获取米游币商品列表"""
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                URL_GOOD_LIST.format(page=page, game=game),
                headers={"User-Agent": UA_MOBILE},
                timeout=15,
            )
        data = res.json()
        if data.get("retcode") == 0:
            return True, data["data"]["list"]
        return False, None
    except Exception:
        return False, None


async def get_address_list(cookies: Dict[str, str]) -> Tuple[bool, Optional[List[Dict]]]:
    """获取用户收货地址列表"""
    headers = get_base_headers(cookies)
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(URL_ADDRESS_LIST, headers=headers, cookies=cookies, timeout=15)
        data = res.json()
        if data.get("retcode") == 0:
            return True, data["data"]["list"]
        return False, None
    except Exception:
        return False, None


# 商品详情 API
URL_GOOD_DETAIL = "https://api-takumi.mihoyo.com/mall/v1/web/goods/detail?app_id=1&point_sn=myb&goods_id={goods_id}"


async def get_good_detail(goods_id: str) -> Tuple[bool, Optional[Dict]]:
    """获取单个商品详情"""
    try:
        async with httpx.AsyncClient() as client:
            res = await client.get(
                URL_GOOD_DETAIL.format(goods_id=goods_id),
                headers={"User-Agent": UA_MOBILE},
                timeout=15,
            )
        data = res.json()
        if data.get("retcode") == 0:
            return True, data["data"]
        return False, None
    except Exception:
        return False, None


async def do_exchange(
    cookies: Dict[str, str],
    goods_id: str,
    uid: str,
    region: str,
    game_biz: str,
    address_id: Optional[str] = None,
    num: int = 1,
) -> Tuple[bool, str, int]:
    """
    执行米游币商品兑换
    返回: (是否成功, 消息, 下次补货时间戳)
    """
    headers = get_base_headers(cookies)
    headers["x-rpc-verify_key"] = "bll8iq97cem8"
    headers["x-rpc-channel"] = "appstore"

    payload: Dict[str, Any] = {
        "app_id": 1,
        "point_sn": "myb",
        "goods_id": goods_id,
        "exchange_num": num,
        "uid": uid,
        "region": region,
        "game_biz": game_biz,
    }
    if address_id:
        payload["address_id"] = address_id

    try:
        async with httpx.AsyncClient() as client:
            res = await client.post(
                URL_EXCHANGE,
                headers=headers,
                cookies=cookies,
                json=payload,
                timeout=15,
            )
        data = res.json()
        retcode = data.get("retcode", -1)
        message = data.get("message", "未知错误")
        
        if retcode == 0:
            return True, "兑换成功 🎉", 0
        
        # 库存不足时获取下次补货时间
        if retcode == -2102:  # 库存不足
            ok, detail = await get_good_detail(goods_id)
            if ok and detail:
                next_time = detail.get("next_time", 0)
                next_num = detail.get("next_num", 0)
                return False, f"库存不足，下次补货: {next_num} 件", next_time
            return False, "库存不足", 0
        
        return False, f"兑换失败: {message} (code={retcode})", 0
    except Exception as e:
        return False, f"兑换请求失败: {e}", 0
