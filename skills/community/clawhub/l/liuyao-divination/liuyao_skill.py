#!/usr/bin/env python3
"""
六爻预测Skill - 提供六爻占卜功能

使用方法：
    from liuyao_skill import LiuyaoSkill

    skill = LiuyaoSkill()
    result = skill.divinate("问财运如何", "男")
    print(result)
"""

import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from initialize import initialization
from utils import (
    deriveChange,
    seekForEgo,
    matchSkyandEarth,
    seekForReps,
    seekForDefects,
    seekForSouls,
    judgeFortune,
)


class LiuyaoSkill:
    """六爻预测Skill主类"""

    # 卦宫名称映射
    PALACE_NAMES = {
        0: "坤宫", 1: "震宫", 2: "坎宫", 3: "兑宫",
        4: "艮宫", 5: "离宫", 6: "巽宫", 7: "乾宫"
    }

    # 卦名映射（三爻卦）
    TRIGRAM_NAMES = {
        0: "坤", 1: "震", 2: "坎", 3: "兑",
        4: "艮", 5: "离", 6: "巽", 7: "乾"
    }

    def __init__(self):
        self.xiang = None

    def divinate(self, question: str, sex: str = "男") -> dict:
        """
        执行六爻预测

        Args:
            question: 所占事项/问题
            sex: 卦主性别（男/女）

        Returns:
            包含完整卦象信息的字典
        """
        # 1. 起卦
        self.xiang = initialization(question, sex)

        # 2. 推导变卦
        deriveChange(self.xiang)

        # 3. 寻世应
        seekForEgo(self.xiang)

        # 4. 纳甲
        matchSkyandEarth(self.xiang)

        # 5. 定六亲
        seekForReps(self.xiang)

        # 6. 缺六亲
        seekForDefects(self.xiang)

        # 7. 配六神
        seekForSouls(self.xiang)

        # 8. 吉凶判断
        judgeFortune(self.xiang)

        return self._format_result()

    def _format_result(self) -> dict:
        """格式化预测结果为字典"""
        x = self.xiang

        # 获取本卦六爻信息（从上到下）
        base_yaos = []
        for i in range(5, -1, -1):  # 从上爻到初爻
            yao = x.base.yaos[i]
            line_type = "⚊" if yao.essence == 1 else "⚋"
            if yao.feature == 0:  # 变爻
                line_type += " ○" if yao.essence == 1 else " ×"

            base_yaos.append({
                'position': ['上爻', '五爻', '四爻', '三爻', '二爻', '初爻'][5-i],
                'index': i + 1,
                'line': line_type,
                'essence': '阳' if yao.essence == 1 else '阴',
                'feature': '老' if yao.feature == 0 else '少',
                'najia': yao.najia,
                'representation': yao.representation.value if yao.representation else None,
                'soul': yao.soul.value if yao.soul else None,
                'is_ego': yao.ego == 1,
                'is_other': yao.other == 1,
            })

        # 获取变卦六爻信息
        change_yaos = None
        if x.change:
            change_yaos = []
            for i in range(5, -1, -1):
                yao = x.change.yaos[i]
                line_type = "⚊" if yao.essence == 1 else "⚋"
                change_yaos.append({
                    'position': ['上爻', '五爻', '四爻', '三爻', '二爻', '初爻'][5-i],
                    'index': i + 1,
                    'line': line_type,
                    'essence': '阳' if yao.essence == 1 else '阴',
                    'representation': yao.representation.value if yao.representation else None,
                })

        # 获取内外卦
        inner_trigram = sum(x.base.yaos[i].essence * (2 ** i) for i in range(3))
        outer_trigram = sum(x.base.yaos[i].essence * (2 ** (i - 3)) for i in range(3, 6))

        # 获取世应位置
        ego_pos = next((i+1 for i, y in enumerate(x.base.yaos) if y.ego == 1), 0)
        other_pos = next((i+1 for i, y in enumerate(x.base.yaos) if y.other == 1), 0)

        # 格式化日期
        year_str = f"{x.year[0].value}{x.year[1].value}" if len(x.year) >= 2 else ""
        month_str = f"{x.month[0].value}{x.month[1].value}" if len(x.month) >= 2 else ""
        day_str = f"{x.day[0].value}{x.day[1].value}" if len(x.day) >= 2 else ""
        hour_str = f"{x.hour[0].value}{x.hour[1].value}" if len(x.hour) >= 2 else ""

        # 格式化空亡
        lacks_str = "".join([e.value for e in x.lacks]) if x.lacks else ""

        # 格式化缺失六亲
        defects_str = [d.value for d in x.defects] if x.defects else []

        return {
            'question': x.question,
            'sex': x.sex,
            'date': {
                'year': year_str,
                'month': month_str,
                'day': day_str,
                'hour': hour_str,
            },
            'lacks': lacks_str,
            'base_gua': {
                'name': f"{self.TRIGRAM_NAMES.get(outer_trigram, '未知')}{self.TRIGRAM_NAMES.get(inner_trigram, '未知')}",
                'inner': self.TRIGRAM_NAMES.get(inner_trigram, '未知'),
                'outer': self.TRIGRAM_NAMES.get(outer_trigram, '未知'),
                'yaos': base_yaos,
            },
            'change_gua': {
                'yaos': change_yaos,
            } if change_yaos else None,
            'palace': self.PALACE_NAMES.get(x.origin, '未知'),
            'ego_position': ego_pos,
            'other_position': other_pos,
            'defects': defects_str,
            'fortune': {
                'level': x.fortune_result.value if x.fortune_result else None,
                'description': x.fortune_description,
            },
            'has_change': x.has_change,
        }

    def format_text(self, result: dict = None) -> str:
        """
        将结果格式化为易读的文本格式

        Args:
            result: divinate方法返回的字典，如果为None则使用最后一次结果

        Returns:
            格式化的文本字符串
        """
        if result is None:
            result = self._format_result()

        lines = []
        lines.append("=" * 50)
        lines.append("【六爻预测结果】")
        lines.append("=" * 50)
        lines.append("")

        # 基本信息
        lines.append(f"占卜问题：{result['question']}")
        lines.append(f"卦主性别：{result['sex']}")
        lines.append("")

        # 日期信息
        d = result['date']
        lines.append(f"日期：{d['year']}年 {d['month']}月 {d['day']}日 {d['hour']}时")
        lines.append(f"旬空：{result['lacks'] or '无'}")
        lines.append("")

        # 本卦
        lines.append("-" * 50)
        lines.append("【本卦】")
        lines.append(f"卦名：{result['base_gua']['name']}")
        lines.append(f"外卦（上）：{result['base_gua']['outer']}")
        lines.append(f"内卦（下）：{result['base_gua']['inner']}")
        lines.append("")

        # 六爻详情
        lines.append("爻象（从上至下）：")
        for yao in result['base_gua']['yaos']:
            mark = ""
            if yao['is_ego']:
                mark = " 【世】"
            elif yao['is_other']:
                mark = " 【应】"

            najia_str = ""
            if yao['najia'] and len(yao['najia']) >= 2:
                najia_str = f" {yao['najia'][0].value}{yao['najia'][1].value}"

            soul_str = f" {yao['soul']}" if yao['soul'] else ""
            reps_str = f"{yao['representation']}" if yao['representation'] else ""

            line = f"  {yao['position']}：{yao['line']:6} {najia_str:4} {reps_str:4} {soul_str:4}{mark}"
            lines.append(line)
        lines.append("")

        # 变卦
        if result['change_gua']:
            lines.append("-" * 50)
            lines.append("【变卦】")
            for yao in result['change_gua']['yaos']:
                line = f"  {yao['position']}：{yao['line']:6} {yao['representation'] or ''}"
                lines.append(line)
            lines.append("")

        # 卦宫信息
        lines.append("-" * 50)
        lines.append("【卦象分析】")
        lines.append(f"卦宫：{result['palace']}")
        lines.append(f"世爻：第{result['ego_position']}爻")
        lines.append(f"应爻：第{result['other_position']}爻")
        if result['defects']:
            lines.append(f"缺失六亲：{', '.join(result['defects'])}")
        else:
            lines.append("六亲：齐全")
        lines.append("")

        # 吉凶判断
        lines.append("=" * 50)
        lines.append(f"【吉凶判断】{result['fortune']['level']}")
        lines.append("=" * 50)
        lines.append(result['fortune']['description'])

        return "\n".join(lines)


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description='六爻预测工具')
    parser.add_argument('question', nargs='?', default='占问前程', help='所占事项')
    parser.add_argument('--sex', '-s', default='男', help='卦主性别（男/女）')

    args = parser.parse_args()

    skill = LiuyaoSkill()
    result = skill.divinate(args.question, args.sex)
    print(skill.format_text(result))


if __name__ == "__main__":
    main()
