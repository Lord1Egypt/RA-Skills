# -*- coding: utf-8 -*-
"""
结果格式化 Agent
"""
from loguru import logger


class FormatterAgent:
    """
    将结构化推荐结果转换为友好的自然语言输出
    """

    def format(self, scene: str, result: dict) -> str:
        """根据场景格式化结果"""
        if scene == "highway":
            return self._format_highway(result)
        elif scene == "hotel":
            return self._format_hotel(result)
        elif scene == "taxi":
            return self._format_taxi(result)
        else:
            return str(result)

    def _format_highway(self, r: dict) -> str:
        exits = r.get("exits", [])
        if not exits:
            return "🚗 未找到附近的高速出口，建议使用导航查看"

        lines = ["🚗 **推荐下高速出口**\n"]
        for i, e in enumerate(exits, 1):
            d = e["distance"] / 1000
            det = e["detour"] / 1000
            lines.append(
                f"**{i}️⃣ {e['name']}**（距你 {d:.1f}km）\n"
                f"　绕行约 {det:.1f}km · 餐饮 ⭐{e['rating']:.1f}\n"
                f"　地址：{e.get('address', '未知')}\n"
                f"　综合得分：{e['score']}分\n"
            )

        lines.append(f"\n💡 推荐【{exits[0]['name']}】综合得分最高")
        return "\n".join(lines)

    def _format_hotel(self, r: dict) -> str:
        hotels = r.get("hotels", [])
        if not hotels:
            return "🏨 附近未找到酒店"

        lines = ["🏨 **推荐住宿**\n"]
        for i, h in enumerate(hotels, 1):
            d = h.get("distance", 0) / 1000
            nd = h.get("next_day_distance", 999999)
            nd_str = f"距次日目的 {nd/1000:.1f}km" if nd < 200000 else "距次日目的较远"
            lines.append(
                f"**{i}️⃣ {h['name']}**\n"
                f"　距你 {d:.1f}km · {nd_str}\n"
                f"　地址：{h.get('address', '未知')}\n"
                f"　综合得分：{h['score']}分\n"
            )

        lines.append(f"\n💡 推荐【{hotels[0]['name']}】综合得分最高")
        return "\n".join(lines)

    def _format_taxi(self, r: dict) -> str:
        points = r.get("points", [])
        if not points:
            return "🚕 附近未找到合适的打车点"

        lines = ["🚕 **推荐打车点**\n"]
        for i, p in enumerate(points, 1):
            d = p["distance"] / 1000
            dd = p.get("dest_distance", 0) / 1000
            lines.append(
                f"**{i}️⃣ {p['name']}**\n"
                f"　步行 {d:.1f}km → 打车 {dd:.1f}km 到目的地\n"
                f"　地址：{p.get('address', '未知')}\n"
                f"　综合得分：{p['score']}分\n"
            )

        lines.append(f"\n💡 推荐【{points[0]['name']}】步行距离最短")
        return "\n".join(lines)
