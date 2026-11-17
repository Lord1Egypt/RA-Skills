#!/usr/bin/env python3
"""
GDPR Compliance Checker — 欧盟通用数据保护条例合规检查工具

使用统一的 compliance_core 模块，提供标准化的 CLI、报告输出和检查引擎。
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from compliance_core import UnifiedCLI, CheckEngine, CheckResult, Severity


class GDPRChecker(CheckEngine):
    """GDPR 合规检查引擎"""

    def __init__(self):
        super().__init__(
            tool_name="GDPR-Compliance",
            regulation="General Data Protection Regulation (GDPR)"
        )
        self._register_all()

    def _register_all(self):
        """注册所有检查项和场景"""
        
        self.register_checker("lawful_basis", self._check_lawful_basis)
        self.register_checker("consent", self._check_consent)
        self.register_checker("privacy_notice", self._check_privacy_notice)
        self.register_checker("data_minimization", self._check_data_minimization)
        self.register_checker("data_subject_rights", self._check_subject_rights)
        self.register_checker("breach_notification", self._check_breach_notification)
        self.register_checker("dpo", self._check_dpo)
        self.register_checker("dpia", self._check_dpia)
        self.register_checker("cross_border", self._check_cross_border)
        self.register_checker("data_protection_by_design", self._check_design)
        self.register_checker("records", self._check_records)
        self.register_checker("security", self._check_security)

        self.register_scenario("basic_compliance", "基础合规",
            ["lawful_basis", "consent", "privacy_notice", "data_subject_rights"])
        self.register_scenario("high_risk_processing", "高风险处理",
            ["lawful_basis", "dpia", "dpo", "data_protection_by_design", "security"])
        self.register_scenario("cross_business", "跨境业务",
            ["lawful_basis", "cross_border", "privacy_notice", "data_subject_rights",
             "breach_notification"])
        self.register_scenario("full_audit", "全面审计",
            ["lawful_basis", "consent", "privacy_notice", "data_minimization",
             "data_subject_rights", "breach_notification", "dpo", "dpia",
             "cross_border", "data_protection_by_design", "records", "security"])

    def _check_lawful_basis(self, data: dict) -> CheckResult:
        """检查合法处理基础"""
        identified_basis = data.get("identified_basis", False)
        bases = data.get("bases", [])

        issues = []
        if not identified_basis: issues.append("未确定数据处理的法律基础")
        if identified_basis and not bases: issues.append("法律基础清单为空")

        return CheckResult(
            check_id="lawful_basis",
            description="数据处理合法基础检查",
            severity=Severity.FAIL if not identified_basis else Severity.PASS,
            passed=identified_basis and len(bases) > 0,
            details="；".join(issues) if issues else f"已确定法律基础: {', '.join(bases) if bases else '待补充'}",
            recommendation="明确每项数据处理活动的法律基础（同意、合同、法定义务等）",
            regulation_ref="GDPR Art.6"
        )

    def _check_consent(self, data: dict) -> CheckResult:
        """检查同意机制"""
        has_unambiguous = data.get("has_unambiguous", False)
        has_withdrawal = data.get("has_withdrawal", False)
        withdrawal_easy = data.get("withdrawal_easy", False)
        no_pre_ticked = data.get("no_pre_ticked", False)
        granular = data.get("granular", False)

        issues = []
        if not has_unambiguous: issues.append("未获取明确同意")
        if not has_withdrawal: issues.append("未提供撤回同意机制")
        if not withdrawal_easy: issues.append("撤回同意不够便捷")
        if not no_pre_ticked: issues.append("使用预勾选框")
        if not granular: issues.append("未提供细颗粒度选择")

        return CheckResult(
            check_id="consent",
            description="用户同意机制检查",
            severity=Severity.FAIL if not has_unambiguous else Severity.WARN,
            passed=has_unambiguous and has_withdrawal,
            details="；".join(issues) if issues else "同意机制合规",
            recommendation="确保同意是自由给予、具体、知情、 unambiguous 的",
            regulation_ref="GDPR Art.7"
        )

    def _check_privacy_notice(self, data: dict) -> CheckResult:
        """检查隐私告知义务"""
        controller_info = data.get("controller_info", False)
        purposes = data.get("purposes", False)
        retention = data.get("retention", False)
        rights_info = data.get("rights_info", False)
        transfers = data.get("transfers", False)

        missing = []
        if not controller_info: missing.append("控制者身份")
        if not purposes: missing.append("处理目的")
        if not retention: missing.append("保留期限")
        if not rights_info: missing.append("权利说明")
        if not transfers: missing.append("跨境传输信息")

        return CheckResult(
            check_id="privacy_notice",
            description="隐私告知义务检查",
            severity=Severity.PASS if len(missing) == 0 else Severity.FAIL,
            passed=len(missing) == 0,
            details="缺失: " + "、".join(missing) if missing else "隐私政策信息完整",
            recommendation="提供简洁透明、易于获取的隐私政策",
            regulation_ref="GDPR Art.13-14"
        )

    def _check_data_minimization(self, data: dict) -> CheckResult:
        """检查数据最小化"""
        adequate = data.get("adequate", False)
        relevant = data.get("relevant", False)
        limited = data.get("limited", False)
        has_retention_schedule = data.get("has_retention_schedule", False)

        issues = []
        if not adequate: issues.append("数据收集超出必要范围")
        if not limited: issues.append("未限制数据保留期限")
        if not has_retention_schedule: issues.append("无数据保留期限计划")

        return CheckResult(
            check_id="data_minimization",
            description="数据最小化原则检查",
            severity=Severity.PASS if len(issues) == 0 else Severity.FAIL,
            passed=len(issues) == 0,
            details="；".join(issues) if issues else "数据最小化原则合规",
            recommendation="只收集处理目的所必需的 data，设定明确的保留期限",
            regulation_ref="GDPR Art.5(1)(c)"
        )

    def _check_subject_rights(self, data: dict) -> CheckResult:
        """检查数据主体权利保障"""
        has_access = data.get("has_access", False)
        has_rectification = data.get("has_rectification", False)
        has_erasure = data.get("has_erasure", False)
        has_portability = data.get("has_portability", False)
        has_restriction = data.get("has_restriction", False)
        has_objection = data.get("has_objection", False)

        missing = []
        if not has_access: missing.append("访问权")
        if not has_rectification: missing.append("更正权")
        if not has_erasure: missing.append("删除权（被遗忘权）")
        if not has_portability: missing.append("数据可携带权")
        if not has_restriction: missing.append("限制处理权")
        if not has_objection: missing.append("反对权")

        return CheckResult(
            check_id="data_subject_rights",
            description="数据主体权利保障检查",
            severity=Severity.FAIL if len(missing) > 0 else Severity.PASS,
            passed=len(missing) == 0,
            details="缺失: " + "、".join(missing) if missing else "数据主体权利保障完整",
            recommendation="建立完整的权利请求处理流程（1个月内响应）",
            regulation_ref="GDPR Art.15-22"
        )

    def _check_breach_notification(self, data: dict) -> CheckResult:
        """检查数据泄露通知义务"""
        has_breach_response = data.get("has_breach_response", False)
        notifies_supervisory = data.get("notifies_supervisory", False)
        notifies_individuals = data.get("notifies_individuals", False)
        response_72h = data.get("response_72h", False)

        issues = []
        if not has_breach_response: issues.append("无数据泄露应急响应计划")
        if not response_72h: issues.append("未能在72小时内通知监管机构")
        if not notifies_supervisory: issues.append("不满足监管机构通知义务")

        return CheckResult(
            check_id="breach_notification",
            description="数据泄露通知义务检查",
            severity=Severity.FAIL if not has_breach_response else Severity.WARN,
            passed=has_breach_response and response_72h,
            details="；".join(issues) if issues else "泄露通知流程合规",
            recommendation="建立72小时内通知监管机构和高风险个人数据泄露的响应流程",
            regulation_ref="GDPR Art.33-34"
        )

    def _check_dpo(self, data: dict) -> CheckResult:
        """检查数据保护官任命"""
        requires_dpo = data.get("requires_dpo", False)
        has_dpo = data.get("has_dpo", False)
        dpo_contact = data.get("dpo_contact", False)
        dpo_independent = data.get("dpo_independent", False)

        issues = []
        if requires_dpo and not has_dpo: issues.append("依法需要任命DPO但未任命")
        if has_dpo and not dpo_contact: issues.append("未公布DPO联系方式")
        if has_dpo and not dpo_independent: issues.append("DPO缺乏独立性保障")

        return CheckResult(
            check_id="dpo",
            description="数据保护官（DPO）任命检查",
            severity=Severity.FAIL if requires_dpo and not has_dpo else Severity.PASS,
            passed=not requires_dpo or (has_dpo and dpo_independent),
            details="；".join(issues) if issues else "DPO安排合规" if not requires_dpo else "DPO已任命且独立",
            recommendation="如符合条件需任命DPO，公告联系方式并保障独立性",
            regulation_ref="GDPR Art.37-39"
        )

    def _check_dpia(self, data: dict) -> CheckResult:
        """检查DPIA（数据保护影响评估）"""
        high_risk = data.get("high_risk", False)
        has_dpia = data.get("has_dpia", False)
        dpia_comprehensive = data.get("dpia_comprehensive", False)
        prior_consultation = data.get("prior_consultation", False)

        issues = []
        if high_risk and not has_dpia: issues.append("高风险处理但未执行DPIA")
        if has_dpia and not dpia_comprehensive: issues.append("DPIA不够全面")
        if high_risk and not prior_consultation: issues.append("未咨询监管机构")

        return CheckResult(
            check_id="dpia",
            description="数据保护影响评估（DPIA）检查",
            severity=Severity.FAIL if high_risk and not has_dpia else Severity.PASS,
            passed=not high_risk or (has_dpia and dpia_comprehensive),
            details="；".join(issues) if issues else "DPIA合规",
            recommendation="高风险处理前必须执行DPIA，必要时事先咨询监管机构",
            regulation_ref="GDPR Art.35-36"
        )

    def _check_cross_border(self, data: dict) -> CheckResult:
        """检查跨境数据传输"""
        transfers_outside_eea = data.get("transfers_outside_eea", False)
        has_safeguards = data.get("has_safeguards", False)
        adequacy_decision = data.get("adequacy_decision", False)
        has_scc = data.get("has_scc", False)
        has_bcr = data.get("has_bcr", False)
        has_tia = data.get("has_tia", False)

        issues = []
        if transfers_outside_eea and not has_safeguards:
            issues.append("跨境传输未采取保障措施")
        if not adequacy_decision and not has_scc and not has_bcr:
            issues.append("未通过充分性认定、SCC或BCR提供保护")
        if not has_tia and transfers_outside_eea:
            issues.append("未完成传输影响评估(TIA)")

        return CheckResult(
            check_id="cross_border",
            description="跨境数据传输合规检查",
            severity=Severity.FAIL if not has_safeguards and transfers_outside_eea else Severity.WARN,
            passed=not transfers_outside_eea or has_safeguards,
            details="；".join(issues) if issues else "跨境传输合规",
            recommendation="使用SCC、BCR或充分性认定作为跨境传输机制，执行TIA",
            regulation_ref="GDPR Art.44-49"
        )

    def _check_design(self, data: dict) -> CheckResult:
        """检查数据保护设计与默认"""
        by_design = data.get("by_design", False)
        by_default = data.get("by_default", False)
        pseudonymization = data.get("pseudonymization", False)
        minimization_default = data.get("minimization_default", False)

        issues = []
        if not by_design: issues.append("未在设计阶段考虑数据保护")
        if not by_default: issues.append("默认未采用最高隐私设置")
        if not pseudonymization: issues.append("未使用假名化等Privacy-Enhancing技术")

        return CheckResult(
            check_id="data_protection_by_design",
            description="数据保护设计与默认检查",
            severity=Severity.WARN if len(issues) > 0 else Severity.PASS,
            passed=by_design and by_default,
            details="；".join(issues) if issues else "数据保护设计和默认合规",
            recommendation="将数据保护嵌入系统设计，默认只处理必要数据",
            regulation_ref="GDPR Art.25"
        )

    def _check_records(self, data: dict) -> CheckResult:
        """检查处理活动记录"""
        maintains_records = data.get("maintains_records", False)
        records_complete = data.get("records_complete", False)
        has_рос = data.get("has_рос", False)

        issues = []
        if not maintains_records: issues.append("未维护处理活动记录(ROPA)")
        if not records_complete: issues.append("处理活动记录不完整")

        return CheckResult(
            check_id="records",
            description="处理活动记录(ROPA)检查",
            severity=Severity.FAIL if not maintains_records else Severity.PASS,
            passed=maintains_records and records_complete,
            details="；".join(issues) if issues else "处理活动记录合规",
            recommendation="维护书面的处理活动记录，包含法定内容",
            regulation_ref="GDPR Art.30"
        )

    def _check_security(self, data: dict) -> CheckResult:
        """检查安全措施"""
        has_encryption = data.get("has_encryption", False)
        has_access_control = data.get("has_access_control", False)
        has_testing = data.get("has_testing", False)
        has_incident_response = data.get("has_incident_response", False)
        has_business_continuity = data.get("has_business_continuity", False)

        issues = []
        if not has_encryption: issues.append("未实施加密")
        if not has_access_control: issues.append("访问控制不足")
        if not has_testing: issues.append("未定期测试安全措施")
        if not has_incident_response: issues.append("无事件响应计划")

        return CheckResult(
            check_id="security",
            description="安全措施充分性检查",
            severity=Severity.FAIL if not has_encryption or not has_access_control else Severity.WARN,
            passed=has_encryption and has_access_control and has_incident_response,
            details="；".join(issues) if issues else "安全措施充足",
            recommendation="实施适当的技术和组织措施（加密、访问控制、定期测试）",
            regulation_ref="GDPR Art.32"
        )


def main():
    engine = GDPRChecker()
    cli = UnifiedCLI(
        tool_name="gdpr-check.py",
        description="GDPR合规检查工具 — 欧盟通用数据保护条例合规评估"
    )
    args = cli.parse_args()

    if args.list_scenarios:
        cli.list_scenarios(engine.get_scenarios())
        return

    report = engine.run(
        scenario=args.scenario,
        interactive=args.interactive,
    )

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            if args.format == "json":
                import json
                json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)
            elif args.format == "markdown":
                from compliance_core.report_core import ReportGenerator
                f.write(ReportGenerator.to_markdown(report.to_dict()))
            else:
                f.write(str(report.to_dict()))
        print(f"\n✅ 报告已保存到: {args.output}")

    cli.print_report(report, fmt=args.format)


if __name__ == "__main__":
    main()
