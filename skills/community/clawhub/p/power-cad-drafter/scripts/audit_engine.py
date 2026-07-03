#!/usr/bin/env python3
"""
power-cad-drafter / scripts/audit_engine.py
电力工程施工图自动审图引擎
依据：公司《电力行业施工图设计规范V1.0》+ GB 50052/50054/50217
"""

import json
import sys
from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class AuditItem:
    category: str
    item: str
    result: bool
    design_value: Any
    required_value: Any
    clause: str
    remark: str = ""


class PowerAuditEngine:
    """10kV及以下供配电工程审图引擎"""

    def __init__(self, design_params: Dict[str, Any]):
        self.dp = design_params
        self.items: List[AuditItem] = []

    def audit_all(self) -> List[AuditItem]:
        self._audit_transformer()
        self._audit_hv_equipment()
        self._audit_lv_equipment()
        self._audit_cables()
        self._audit_grounding()
        self._audit_substation()
        self._audit_metering()
        self._audit_reactive_power()
        self._audit_protection()
        return self.items

    def _audit_transformer(self):
        tx_type = self.dp.get("transformer_type", "dry")
        tx_cap = self.dp.get("transformer_capacity", 0)
        wiring = self.dp.get("wiring_group", "")
        usage = self.dp.get("usage_type", "public")

        max_cap = 1250 if usage == "public" else 2500 if tx_type == "dry" else 630 if usage == "public" else 1250
        self.items.append(AuditItem(
            category="变压器", item="单台变压器容量",
            result=tx_cap <= max_cap,
            design_value=f"{tx_cap}kVA", required_value=f"≤{max_cap}kVA ({tx_type}, {usage})",
            clause="DBJ45-004-2012 4.1.2 / 南网典设 4.7.2"))

        self.items.append(AuditItem(
            category="变压器", item="接线组别",
            result=wiring.upper() in ("D,YN11", "DYN11"),
            design_value=wiring, required_value="D,yn11",
            clause="GB 50052 7.0.7 / 南网典设 4.7.2"))

        if tx_cap < 630:
            req_uk = 4.0
        else:
            req_uk = 6.0 if tx_type == "dry" else 4.5
        uk = self.dp.get("short_circuit_impedance", 0)
        self.items.append(AuditItem(
            category="变压器", item="短路阻抗",
            result=abs(uk - req_uk) < 0.1 if uk else True,
            design_value=f"{uk}%" if uk else "未标注", required_value=f"{req_uk}%",
            clause="南网典设 4.7.2"))

    def _audit_hv_equipment(self):
        ip = self.dp.get("hv_switchgear_ip", "")
        five_prevention = self.dp.get("five_prevention", False)
        breaker_type = self.dp.get("hv_switch_type", "")

        try:
            ip_num = int(ip.replace("IP", "").replace("X", "0")) if ip else 0
            ip_pass = ip_num >= 40
        except:
            ip_pass = False
        self.items.append(AuditItem(
            category="高压开关柜", item="外壳防护等级",
            result=ip_pass, design_value=ip, required_value="≥IP4X",
            clause="南网典设 4.7.1"))

        self.items.append(AuditItem(
            category="高压开关柜", item="五防联锁功能",
            result=five_prevention,
            design_value="有" if five_prevention else "无", required_value="必须具备",
            clause="南网典设 4.7.1 / GB 50060"))

        tx_cap = self.dp.get("transformer_capacity", 0)
        tx_count = self.dp.get("transformer_count", 1)
        tx_type = self.dp.get("transformer_type", "dry")
        limit = 800 if tx_type == "dry" else 630
        need_breaker = tx_cap > limit or tx_count > 2
        if need_breaker:
            self.items.append(AuditItem(
                category="高压开关柜", item="进线开关选型",
                result=breaker_type in ("breaker", "真空断路器"),
                design_value=breaker_type, required_value="断路器（容量超限或台数>2）",
                clause="南网典设 4.8.2"))

    def _audit_lv_equipment(self):
        tx_cap = self.dp.get("transformer_capacity", 0)
        breaker_ka = self.dp.get("lv_breaker_kA", 0)
        req_ka = 35 if tx_cap <= 800 else 50
        self.items.append(AuditItem(
            category="低压开关柜", item="断路器短路分断能力",
            result=breaker_ka >= req_ka,
            design_value=f"{breaker_ka}kA", required_value=f"≥{req_ka}kA",
            clause="南网典设 4.7.6 / 规范V1.0 4.3.2"))

        tx_count = self.dp.get("transformer_count", 1)
        has_bus_coupler = self.dp.get("lv_bus_coupler", False)
        self.items.append(AuditItem(
            category="低压开关柜", item="0.4kV母联开关",
            result=tx_count < 2 or has_bus_coupler,
            design_value="有" if has_bus_coupler else "无",
            required_value="≥2台变压器时必须设置" if tx_count >= 2 else "无需设置",
            clause="DBJ45-004-2012 3.3.5 / 规范V1.0 3.2.2"))

    def _audit_cables(self):
        hv_cable = self.dp.get("hv_cable_section", 0)
        lv_main = self.dp.get("lv_main_cable_section", 0)
        service_line = self.dp.get("service_line_section", 0)

        self.items.append(AuditItem(
            category="电缆", item="高压电缆截面",
            result=hv_cable >= 70,
            design_value=f"{hv_cable}mm²" if hv_cable else "未标注", required_value="≥70mm²（铜芯）",
            clause="规范V1.0 5.4.1"))

        self.items.append(AuditItem(
            category="电缆", item="低压主干电缆截面",
            result=lv_main >= 150,
            design_value=f"{lv_main}mm²" if lv_main else "未标注", required_value="≥150mm²（铜芯）",
            clause="规范V1.0 5.4.2（强制性）"))

        self.items.append(AuditItem(
            category="电缆", item="入户线截面",
            result=service_line >= 10,
            design_value=f"{service_line}mm²" if service_line else "未标注", required_value="≥10mm²（铜芯，强制性）",
            clause="DBJ45-004-2012 4.1.1 / 规范V1.0 5.4.2"))

        cable_insulation = self.dp.get("cable_insulation", "")
        is_public = self.dp.get("building_type", "") in ("high_rise", "public")
        self.items.append(AuditItem(
            category="电缆", item="电缆绝缘类型（公共/高层建筑）",
            result=not is_public or "低烟无卤" in cable_insulation or "WDZ" in cable_insulation,
            design_value=cable_insulation, required_value="阻燃低烟无卤（WDZ-YJY）",
            clause="GB 50217 3.3.7 / 规范V1.0 5.2.1"))

    def _audit_grounding(self):
        grounding_type = self.dp.get("grounding_system", "")
        r_value = self.dp.get("grounding_resistance", 999)
        tx_cap = self.dp.get("transformer_capacity", 0)
        substation_in_building = self.dp.get("substation_in_building", False)

        req_g = "TN-S" if substation_in_building else "TN-S 或 TN-C-S"
        g_pass = "TN-S" in grounding_type.upper()
        if not substation_in_building:
            g_pass = g_pass or "TN-C-S" in grounding_type.upper()
        self.items.append(AuditItem(
            category="接地", item="接地系统型式",
            result=g_pass, design_value=grounding_type, required_value=req_g,
            clause="GB 50054 7.7.8 / 规范V1.0 7.3.1（建筑物内强制TN-S）"))

        req_r = 4 if tx_cap >= 100 else 10
        self.items.append(AuditItem(
            category="接地", item="接地电阻",
            result=r_value <= req_r,
            design_value=f"{r_value}Ω", required_value=f"≤{req_r}Ω",
            clause="规范V1.0 7.3.2"))

        self.items.append(AuditItem(
            category="接地", item="建筑物内严禁TN-C",
            result="TN-C" not in grounding_type.upper() or not substation_in_building,
            design_value=grounding_type, required_value="建筑物内严禁TN-C",
            clause="GB 50054 3.1.4 / 规范V1.0 7.3.1（强制性）"))

    def _audit_substation(self):
        fire_rating = self.dp.get("fire_rating", "")
        aisle_front = self.dp.get("aisle_front_width", 0)
        drawer_type = self.dp.get("drawer_type_switchgear", False)
        bare_height = self.dp.get("bare_conductor_height", 0)

        self.items.append(AuditItem(
            category="配电室", item="屋顶耐火等级",
            result="二" in fire_rating or "一" in fire_rating,
            design_value=fire_rating, required_value="≥二级",
            clause="DBJ45-004-2012 4.1.2 / 规范V1.0 6.2.1"))

        req_aisle = 1.8 if drawer_type else 1.5
        self.items.append(AuditItem(
            category="配电室", item="屏前操作通道",
            result=aisle_front >= req_aisle,
            design_value=f"{aisle_front}m", required_value=f"≥{req_aisle}m",
            clause="GB 50054 4.2.5 / 规范V1.0 6.2.3"))

        self.items.append(AuditItem(
            category="配电室", item="裸带电体距地高度",
            result=bare_height >= 2.5,
            design_value=f"{bare_height}m", required_value="≥2.5m",
            clause="GB 50054 4.2.6（强制性）"))

        not_lowest = self.dp.get("substation_not_lowest_floor", True)
        self.items.append(AuditItem(
            category="配电室", item="配电站不应设在地下最底层",
            result=not_lowest,
            design_value="是" if not_lowest else "否", required_value="不应设在地下最底层",
            clause="DBJ45-004-2012 3.4.5（强制性）"))

    def _audit_metering(self):
        meter_height = self.dp.get("meter_height", 0)
        floors = self.dp.get("building_floors", 0)
        meter_per_3to6 = self.dp.get("meter_every_3to6_floors", False)

        self.items.append(AuditItem(
            category="电能计量", item="电能表安装高度",
            result=0.8 <= meter_height <= 1.8,
            design_value=f"{meter_height}m", required_value="0.8~1.8m",
            clause="DBJ45-004-2012 3.6.6 / 规范V1.0 8.2.3"))

        if floors >= 12:
            self.items.append(AuditItem(
                category="电能计量", item="高层电表箱分层设置",
                result=meter_per_3to6,
                design_value="是" if meter_per_3to6 else "否", required_value="12层及以上每3~6层设一处",
                clause="DBJ45-004-2012 3.6.6"))

    def _audit_reactive_power(self):
        tx_cap = self.dp.get("transformer_capacity", 0)
        comp_cap = self.dp.get("compensation_capacity", 0)
        cos_phi = self.dp.get("power_factor", 0)

        ratio = (comp_cap / tx_cap * 100) if tx_cap else 0
        self.items.append(AuditItem(
            category="无功补偿", item="补偿容量比例",
            result=20 <= ratio <= 40,
            design_value=f"{ratio:.1f}% ({comp_cap}kvar / {tx_cap}kVA)", required_value="20%~40%",
            clause="规范V1.0 9.1.2"))

        self.items.append(AuditItem(
            category="无功补偿", item="功率因数",
            result=cos_phi >= 0.9,
            design_value=f"{cos_phi}", required_value="≥0.9",
            clause="南网典设 4.11.1 / 规范V1.0 9.1.1"))

    def _audit_protection(self):
        has_protection = self.dp.get("protection_configured", False)
        self.items.append(AuditItem(
            category="继电保护", item="保护配置",
            result=has_protection,
            design_value="已配置" if has_protection else "未配置", required_value="必须配置",
            clause="南网典设 4.9 / 规范V1.0 第10章"))

    def generate_report(self) -> str:
        lines = [
            f"# 审图报告：{self.dp.get('project_name', '未命名工程')}",
            "",
            "| 检查类别 | 检查项 | 结果 | 设计值 | 规范要求 | 依据条文 | 备注 |",
            "|---------|--------|------|--------|---------|---------|------|",
        ]
        pass_count = sum(1 for it in self.items if it.result)
        for it in self.items:
            icon = "✅ 通过" if it.result else "❌ 不通过"
            remark = it.remark if it.remark else ("符合要求" if it.result else "需整改")
            lines.append(
                f"| {it.category} | {it.item} | {icon} | {it.design_value} | {it.required_value} | {it.clause} | {remark} |")
        lines.append("")
        lines.append(f"**总结：共 {len(self.items)} 项检查，通过 {pass_count} 项，不通过 {len(self.items)-pass_count} 项。**")
        lines.append("")
        if pass_count < len(self.items):
            lines.append("## 整改建议")
            for it in self.items:
                if not it.result:
                    lines.append(f"- **{it.category} — {it.item}**：设计值为 `{it.design_value}`，应调整为 `{it.required_value}`。依据：{it.clause}")
        return "\n".join(lines)


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            params = json.load(f)
    else:
        params = {
            "project_name": "XX小区配电工程",
            "transformer_type": "dry",
            "transformer_capacity": 800,
            "transformer_count": 2,
            "wiring_group": "D,yn11",
            "short_circuit_impedance": 6.0,
            "hv_switchgear_ip": "IP4X",
            "five_prevention": True,
            "hv_switch_type": "breaker",
            "lv_breaker_kA": 50,
            "lv_bus_coupler": True,
            "hv_cable_section": 95,
            "lv_main_cable_section": 240,
            "service_line_section": 10,
            "cable_insulation": "WDZ-YJY",
            "building_type": "high_rise",
            "grounding_system": "TN-S",
            "grounding_resistance": 3.5,
            "substation_in_building": True,
            "fire_rating": "二级",
            "aisle_front_width": 1.6,
            "drawer_type_switchgear": True,
            "bare_conductor_height": 2.8,
            "substation_not_lowest_floor": True,
            "meter_height": 1.2,
            "building_floors": 18,
            "meter_every_3to6_floors": True,
            "compensation_capacity": 240,
            "power_factor": 0.92,
            "protection_configured": True,
            "usage_type": "public",
        }

    engine = PowerAuditEngine(params)
    engine.audit_all()
    report = engine.generate_report()

    output_path = sys.argv[2] if len(sys.argv) > 2 else "/Users/wnep/.openclaw/workspace/audit_report.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"[Audit] 审图报告已生成：{output_path}")
    print(f"[Audit] 总计 {len(engine.items)} 项，通过 {sum(1 for i in engine.items if i.result)} 项")


if __name__ == "__main__":
    main()
