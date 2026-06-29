"""
Riot API 客户端 - 封装 RiotWatcher，提供高层API调用
"""
from riotwatcher import LolWatcher, ApiError
from config_manager import get_api_key, get_routing

# 静态英雄数据缓存（基于 Community Dragon 的简化版）
CHAMPION_NAMES = {
    1: "安妮", 2: "奥拉夫", 3: "加里奥", 4: "崔斯特", 5: "赵信",
    6: "厄加特", 7: "乐芙兰", 8: "弗拉基米尔", 9: "费德提克", 10: "凯尔",
    11: "易", 12: "阿利斯塔", 13: "瑞兹", 14: "赛恩", 15: "希维尔",
    16: "索拉卡", 17: "提莫", 18: "崔丝塔娜", 19: "沃里克", 20: "努努和威朗普",
    21: "厄运小姐", 22: "艾希", 23: "泰达米尔", 24: "贾克斯", 25: "莫甘娜",
    26: "基兰", 27: "辛吉德", 28: "伊芙琳", 29: "图奇", 30: "卡尔萨斯",
    31: "科加斯", 32: "阿木木", 33: "拉莫斯", 34: "艾尼维亚", 35: "萨科",
    36: "蒙多医生", 37: "娑娜", 38: "卡萨丁", 39: "艾瑞莉娅", 40: "迦娜",
    41: "普朗克", 42: "库奇", 43: "卡尔玛", 44: "塔里克", 45: "维迦",
    48: "特朗德尔", 50: "斯维因", 51: "凯特琳", 53: "布里茨", 54: "墨菲特",
    55: "卡特琳娜", 56: "魔腾", 57: "茂凯", 58: "雷克顿", 59: "嘉文四世",
    60: "伊莉丝", 61: "奥莉安娜", 62: "孙悟空", 63: "布兰德", 64: "李青",
    67: "薇恩", 68: "兰博", 69: "卡西奥佩娅", 72: "斯卡纳", 74: "黑默丁格",
    75: "内瑟斯", 76: "奈德丽", 77: "乌迪尔", 78: "波比", 79: "古拉加斯",
    80: "潘森", 81: "伊泽瑞尔", 82: "莫德凯撒", 83: "约里克", 84: "阿卡丽",
    85: "凯南", 86: "盖伦", 89: "蕾欧娜", 90: "玛尔扎哈", 91: "塔隆",
    92: "锐雯", 96: "克格莫", 98: "慎", 99: "拉克丝", 101: "泽拉斯",
    102: "希瓦娜", 103: "阿狸", 104: "格雷福斯", 105: "菲兹", 106: "沃利贝尔",
    107: "雷恩加尔", 110: "韦鲁斯", 111: "诺提勒斯", 112: "维克托", 113: "瑟庄妮",
    114: "菲奥娜", 115: "吉格斯", 117: "璐璐", 119: "德莱文", 120: "赫卡里姆",
    121: "卡兹克", 122: "德莱厄斯", 126: "杰斯", 127: "丽桑卓", 131: "黛安娜",
    133: "奎因", 134: "辛德拉", 136: "奥瑞利安·索尔", 141: "凯隐", 142: "佐伊",
    143: "婕拉", 145: "卡莎", 147: "塞拉芬", 150: "纳尔", 154: "扎克",
    157: "亚索", 161: "维克兹", 163: "塔莉垭", 164: "卡蜜尔", 166: "艾翁",
    200: "卑尔维斯", 201: "布隆", 202: "烬", 203: "千珏", 221: "金克丝",
    222: "金克丝", 223: "塔姆", 234: "薇古丝", 235: "赛娜", 236: "卢锡安",
    238: "塞拉斯", 240: "克烈", 245: "艾克", 246: "琪亚娜", 254: "蔚",
    266: "亚托克斯", 267: "娜美", 268: "阿兹尔", 350: "悠米", 360: "莎弥拉",
    412: "锤石", 420: "雷欧娜", 421: "雷克塞", 427: "艾翁", 429: "卡莉丝塔",
    432: "巴德", 497: "洛", 498: "霞", 516: "奥恩", 517: "赛拉斯",
    518: "妮蔻", 523: "厄斐琉斯", 526: "芮尔", 555: "派克", 777: "永恩",
    875: "萨勒芬妮", 876: "格温", 887: "莉莉娅", 888: "费伊", 895: "薇克托",
    897: "阿克尚", 901: "泽丽", 902: "芮娜塔", 910: "卑尔维斯", 950: "纳亚菲利",
}


def get_champion_name(champion_id: int) -> str:
    """根据英雄ID获取中文名称"""
    return CHAMPION_NAMES.get(champion_id, f"英雄#{champion_id}")


class RiotClient:
    """Riot Games API 客户端"""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or get_api_key()
        if not self.api_key:
            raise ValueError(
                "未找到 Riot API Key！\n"
                "请通过以下方式配置：\n"
                "1. 环境变量: export RIOT_API_KEY=\"RGAPI-xxx\"\n"
                "2. 或运行时提供 --api-key 参数"
            )
        self.watcher = LolWatcher(self.api_key)

    def get_summoner_by_name(self, region: str, name: str, tag: str) -> dict:
        """通过 Riot ID (name#tag) 查询召唤师"""
        try:
            routing = get_routing(region)
            account = self.watcher.account.by_riot_id(routing, name, tag)
            summoner = self.watcher.summoner.by_puuid(region, account["puuid"])
            return {
                "account": account,
                "summoner": summoner,
            }
        except ApiError as e:
            if e.response.status_code == 404:
                raise ValueError(f"未找到玩家 {name}#{tag}（区域: {region}）")
            elif e.response.status_code == 403:
                raise ValueError(
                    "API Key 无效或已过期！\n"
                    "开发版 Key 每24小时过期，请去 developer.riotgames.com 重新获取"
                )
            raise

    def get_ranked_stats(self, region: str, summoner_id: str) -> list:
        """获取排位数据"""
        try:
            entries = self.watcher.league.by_summoner(region, summoner_id)
            return entries
        except ApiError as e:
            if e.response.status_code == 404:
                return []  # 无排位数据
            raise

    def get_match_history(self, region: str, puuid: str, count: int = 20,
                          queue: int = None) -> list:
        """获取对局历史（仅返回 match IDs）"""
        routing = get_routing(region)
        kwargs = {"count": min(count, 100)}
        if queue is not None:
            kwargs["queue"] = queue
        try:
            match_ids = self.watcher.match.by_puuid(routing, puuid, **kwargs)
            return match_ids
        except ApiError as e:
            raise

    def get_match_detail(self, region: str, match_id: str) -> dict:
        """获取单场对局详情"""
        routing = get_routing(region)
        try:
            match = self.watcher.match.by_id(routing, match_id)
            return match
        except ApiError as e:
            raise

    def get_champion_masteries(self, region: str, puuid: str, count: int = 10) -> list:
        """获取英雄熟练度"""
        try:
            masteries = self.watcher.champion_mastery.by_puuid(region, puuid, count=count)
            return masteries
        except ApiError as e:
            raise

    def get_match_details_batch(self, region: str, match_ids: list,
                                 puuid: str) -> list:
        """批量获取对局详情并提取当前玩家的数据"""
        matches = []
        for mid in match_ids:
            try:
                match = self.get_match_detail(region, mid)
                player_data = self._extract_player_data(match, puuid)
                if player_data:
                    matches.append(player_data)
            except ApiError:
                continue  # 跳过获取失败的对局
        return matches

    def _extract_player_data(self, match: dict, puuid: str) -> dict:
        """从完整对局数据中提取特定玩家的数据"""
        info = match.get("info", {})
        participants = info.get("participants", [])

        player = None
        for p in participants:
            if p.get("puuid") == puuid:
                player = p
                break

        if not player:
            return None

        # 计算队伍总KDA
        team_id = player.get("teamId")
        team_kills = sum(
            p.get("kills", 0) for p in participants if p.get("teamId") == team_id
        )

        return {
            "match_id": match.get("metadata", {}).get("matchId", ""),
            "game_duration": info.get("gameDuration", 0),
            "game_mode": info.get("gameMode", ""),
            "game_type": info.get("gameType", ""),
            "win": player.get("win", False),
            "champion_id": player.get("championId", 0),
            "champion_name": player.get("championName", ""),
            "kills": player.get("kills", 0),
            "deaths": player.get("deaths", 0),
            "assists": player.get("assists", 0),
            "kda": self._calc_kda(
                player.get("kills", 0),
                player.get("deaths", 0),
                player.get("assists", 0),
            ),
            "kill_participation": self._calc_kp(
                player.get("kills", 0),
                player.get("assists", 0),
                team_kills,
            ),
            "cs": player.get("totalMinionsKilled", 0)
                  + player.get("neutralMinionsKilled", 0),
            "cs_per_min": 0,
            "gold_earned": player.get("goldEarned", 0),
            "damage_dealt": player.get("totalDamageDealtToChampions", 0),
            "damage_taken": player.get("totalDamageTaken", 0),
            "vision_score": player.get("visionScore", 0),
            "item_ids": [
                player.get(f"item{i}", 0) for i in range(7)
            ],
            "summoner_spells": [
                player.get("summoner1Id", 0),
                player.get("summoner2Id", 0),
            ],
            "level": player.get("champLevel", 0),
            "team_position": player.get("teamPosition", ""),
            "lane": player.get("lane", ""),
        }

    @staticmethod
    def _calc_kda(kills: int, deaths: int, assists: int) -> float:
        """计算 KDA"""
        if deaths == 0:
            return round(kills + assists, 1)
        return round((kills + assists) / deaths, 2)

    @staticmethod
    def _calc_kp(kills: int, assists: int, team_kills: int) -> int:
        """计算参团率 (%)"""
        if team_kills == 0:
            return 0
        return round((kills + assists) / team_kills * 100)


def create_client(api_key: str = None) -> RiotClient:
    """创建 RiotClient 实例"""
    return RiotClient(api_key)
