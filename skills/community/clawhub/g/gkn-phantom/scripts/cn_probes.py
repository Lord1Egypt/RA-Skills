#!/usr/bin/env python3
"""CN Component Probes — domestic OA / component unauthorized-access library (v1.0.0).

Chinese enterprise software dominates domestic SRC high-severity reports, but
official nuclei templates barely cover it. This module turns accumulated SRC
knowledge into a structured probe library:

  Component       | High-value unauthorized surfaces
  ----------------+-------------------------------------------------------------
  泛微 e-cology   | weaver.* interfaces, BeanShell servlet, SSO login, /services/
  泛微 e-office   | /eoffice10/ API
  致远 A8/seeyon  | htmlofficeservlet, wpsAssistServlet, getSessionList
  通达 OA         | /ispirit/, /module/ interfaces
  用友 NC/GRP     | ~ic servlets, uapws services
  禅道 ZenTao     | getconfig leak
  JeecgBoot       | jmreport queryFieldBySql (one-shot SQLi verify), /sys/
  若依 RuoYi      | druid variants (prod-api/dev-api), /system/, /v1/
  帆软 FineReport | /decision/ console
  亿邮/金蝶/蓝凌/红帆/万户 | fingerprints + known endpoints

Probe dict shape is compatible with quick_combat.QUICK_PROBES, extended with:
  - "severity"     — override the default baseline severity
  - "method"/"post_body"/"post_content_type" — POST-based one-shot verifiers
  - "not_patterns" — body blacklist that suppresses soft-404 false positives

Importable:
  from cn_probes import CN_PROBES, probe_cn_components
CLI:
  python cn_probes.py --targets https://a.test,https://b.test
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils import dump_json


CN_PROBES = [
    # ==== 泛微 e-cology =====================================================
    {
        "type": "component_exposure",
        "name": "Weaver e-cology BeanShell servlet (RCE point)",
        "paths": [
            "/bsh.servlet.BshServlet",
            "/weaver/bsh.servlet.BshServlet",
        ],
        "check": "pattern",
        "patterns": ["BeanShell", "beanshell", "bsh.servlet.BshServlet"],
        "not_patterns": ["404", "Not Found"],
        "severity": "critical",
    },
    {
        "type": "sqli",
        "name": "Weaver e-cology Ssologin.jsp (unauth SQLi point)",
        "paths": ["/mobile/plugin/Ssologin.jsp"],
        "check": "pattern",
        "patterns": ["Ssologin", "ssoLogin", "ecology"],
        "not_patterns": ["404"],
        "severity": "high",
    },
    {
        "type": "component_exposure",
        "name": "Weaver e-cology /services/ AXIS WSDL exposure",
        "paths": ["/services/", "/services/listServices"],
        "check": "pattern",
        "patterns": ["wsdl", "WSDL", "axis", "Axis"],
        "not_patterns": ["404"],
        "severity": "high",
    },
    # ==== 泛微 e-office =====================================================
    {
        "type": "component_exposure",
        "name": "Weaver e-office fingerprint",
        "paths": ["/eoffice10/", "/eoffice/"],
        "check": "pattern",
        "patterns": ["eoffice", "e-office"],
        "not_patterns": ["404"],
        "severity": "medium",
    },
    {
        "type": "component_exposure",
        "name": "Weaver e-office10 server API exposure",
        "paths": ["/eoffice10/server/api/"],
        "check": "status",
        "status_codes": [200],
        "not_patterns": ["404", "Not Found"],
        "severity": "high",
    },
    # ==== 致远 seeyon =======================================================
    {
        "type": "component_exposure",
        "name": "Seeyon getSessionList.jsp unauth session disclosure",
        "paths": ["/seeyon/getSessionList.jsp"],
        "check": "pattern",
        "patterns": ["session", "Session", "seeyon"],
        "not_patterns": ["404"],
        "severity": "high",
    },
    {
        "type": "component_exposure",
        "name": "Seeyon htmlofficeservlet (unauth file upload point)",
        "paths": ["/seeyon/htmlofficeservlet"],
        "check": "status",
        "status_codes": [200, 500],
        "not_patterns": ["404"],
        "severity": "high",
    },
    {
        "type": "component_exposure",
        "name": "Seeyon wpsAssistServlet (arbitrary file read point)",
        "paths": ["/seeyon/wpsAssistServlet"],
        "check": "status",
        "status_codes": [200, 500],
        "not_patterns": ["404"],
        "severity": "high",
    },
    {
        "type": "component_exposure",
        "name": "Seeyon A8 fingerprint",
        "paths": ["/seeyon/main.do", "/seeyon/login.jsp", "/login.jsp"],
        "check": "pattern",
        "patterns": ["seeyon", "Seeyon", "致远"],
        "severity": "low",
    },
    # ==== 通达 OA ===========================================================
    {
        "type": "component_exposure",
        "name": "TongDa OA fingerprint",
        "paths": ["/general/index.php", "/logincheck.php", "/ispirit/logout.php"],
        "check": "pattern",
        "patterns": ["TONGDA", "tongda", "通达", "td_", "ispirit"],
        "severity": "low",
    },
    {
        "type": "component_exposure",
        "name": "TongDa OA unauthorized module interfaces",
        "paths": [
            "/ispirit/interface/gateway.php",
            "/module/appbuilder/login.php",
            "/mac/gateway.php",
        ],
        "check": "status",
        "status_codes": [200],
        "not_patterns": ["404", "Not Found", "error", "未找到"],
        "severity": "high",
    },
    {
        "type": "component_exposure",
        "name": "TongDa OA module get.php (file read point)",
        "paths": ["/module/udf/get.php"],
        "check": "status",
        "status_codes": [200],
        "not_patterns": ["404", "Not Found"],
        "severity": "high",
    },
    # ==== 用友 ==============================================================
    {
        "type": "component_exposure",
        "name": "Yonyou NC BeanShell servlet (RCE point)",
        "paths": ["/servlet/~ic/bsh.servlet.BshServlet"],
        "check": "pattern",
        "patterns": ["BeanShell", "beanshell", "bsh.servlet.BshServlet"],
        "not_patterns": ["404"],
        "severity": "critical",
    },
    {
        "type": "component_exposure",
        "name": "Yonyou NC ManagerServlet (info disclosure)",
        "paths": ["/servlet/~ic/nc.bs.framework.mx.manager.ManagerServlet"],
        "check": "pattern",
        "patterns": ["nc.bs.framework", "version"],
        "not_patterns": ["404"],
        "severity": "high",
    },
    {
        "type": "component_exposure",
        "name": "Yonyou uapws service exposure",
        "paths": ["/uapws/service/", "/uapws/"],
        "check": "pattern",
        "patterns": ["wsdl", "WSDL", "uapws"],
        "not_patterns": ["404"],
        "severity": "high",
    },
    {
        "type": "component_exposure",
        "name": "Yonyou fingerprint",
        "paths": ["/portal/", "/login.jsp"],
        "check": "pattern",
        "patterns": ["用友", "yonyou", "Yonyou", "YONYOU", "nc.ui"],
        "severity": "low",
    },
    # ==== 禅道 ==============================================================
    {
        "type": "info_leak",
        "name": "ZenTao getconfig information disclosure",
        "paths": [
            "/www/index.php?mode=getconfig",
            "/zentao/index.php?mode=getconfig",
        ],
        "check": "pattern",
        "patterns": ["zentao", "ZenTao", 'version'],
        "not_patterns": ["404"],
        "severity": "medium",
    },
    {
        "type": "component_exposure",
        "name": "ZenTao fingerprint",
        "paths": ["/zentao/", "/www/", "/user-login.html"],
        "check": "pattern",
        "patterns": ["zentao", "ZenTao", "禅道"],
        "severity": "low",
    },
    # ==== JeecgBoot =========================================================
    {
        "type": "sqli",
        "name": "JeecgBoot jmreport queryFieldBySql SQL injection (one-shot verify)",
        "paths": [
            "/jeecg-boot/jmreport/queryFieldBySql",
            "/api/jmreport/queryFieldBySql",
        ],
        "method": "POST",
        "post_body": '{"sql": "select \'GKNVERIFY\'"}',
        "post_content_type": "application/json",
        "check": "pattern",
        "patterns": ["GKNVERIFY"],
        "severity": "critical",
    },
    {
        "type": "component_exposure",
        "name": "JeecgBoot jmreport list exposure",
        "paths": [
            "/jeecg-boot/jmreport/list",
            "/api/jmreport/list",
        ],
        "check": "pattern",
        "patterns": ["jmreport", "total", "records"],
        "not_patterns": ["404", "Not Found"],
        "severity": "high",
    },
    {
        "type": "component_exposure",
        "name": "JeecgBoot /sys/ unauth access",
        "paths": [
            "/jeecg-boot/sys/user/list",
            "/api/sys/user/list",
        ],
        "check": "pattern",
        "patterns": ["username", "records", "total", "jeecg"],
        "not_patterns": ["404", "Not Found", "login", "Login"],
        "severity": "high",
    },
    {
        "type": "component_exposure",
        "name": "JeecgBoot fingerprint",
        "paths": ["/jeecg-boot/", "/jeecg-boot/sys/login"],
        "check": "pattern",
        "patterns": ["jeecg", "Jeecg", "JEECG"],
        "severity": "low",
    },
    # ==== 若依 RuoYi ========================================================
    {
        "type": "component_exposure",
        "name": "RuoYi Druid monitoring console variants",
        "paths": [
            "/prod-api/druid/index.html",
            "/api/druid/index.html",
            "/dev-api/druid/index.html",
        ],
        "check": "pattern",
        "patterns": ["Druid Stat Index", "druid-login", "Druid"],
        "not_patterns": ["404"],
        "severity": "high",
    },
    {
        "type": "component_exposure",
        "name": "RuoYi unauth user list",
        "paths": [
            "/system/user/list",
            "/prod-api/system/user/list",
            "/v1/user/list",
        ],
        "check": "pattern",
        "patterns": ["userName", "total", "rows"],
        "not_patterns": ["404", "Not Found", "login", "Login"],
        "severity": "high",
    },
    {
        "type": "component_exposure",
        "name": "RuoYi fingerprint",
        "paths": ["/", "/login"],
        "check": "pattern",
        "patterns": ["若依", "RuoYi", "ruoyi"],
        "severity": "low",
    },
    # ==== 帆软 FineReport ===================================================
    {
        "type": "component_exposure",
        "name": "FineReport decision console",
        "paths": [
            "/decision/login",
            "/webroot/decision/login",
            "/webroot/decision/",
        ],
        "check": "pattern",
        "patterns": ["FineReport", "finereport", "帆软", "decision"],
        "not_patterns": ["404"],
        "severity": "medium",
    },
    # ==== 亿邮 ==============================================================
    {
        "type": "component_exposure",
        "name": "Eyou mail apilogin.php (RCE point)",
        "paths": ["/apilogin.php"],
        "check": "pattern",
        "patterns": ["eyou", "Eyou", "亿邮"],
        "not_patterns": ["404"],
        "severity": "high",
    },
    # ==== 金蝶 ==============================================================
    {
        "type": "component_exposure",
        "name": "Kingdee K3Cloud exposure",
        "paths": ["/K3Cloud/", "/kingdee/", "/K3Cloud/Login.aspx"],
        "check": "pattern",
        "patterns": ["K3Cloud", "k3cloud", "金蝶", "kingdee", "Kingdee"],
        "not_patterns": ["404"],
        "severity": "medium",
    },
    # ==== 蓝凌 ==============================================================
    {
        "type": "component_exposure",
        "name": "Landray OA sysSearchMain / custom.jsp (SQLi & file-write points)",
        "paths": [
            "/sys/search/sys_search_main/sysSearchMain.do",
            "/sys/ui/extend/varkind/custom.jsp",
        ],
        "check": "pattern",
        "patterns": ["landray", "Landray", "蓝凌", "sys_search"],
        "not_patterns": ["404"],
        "severity": "high",
    },
    {
        "type": "component_exposure",
        "name": "Landray OA fingerprint",
        "paths": ["/login.do"],
        "check": "pattern",
        "patterns": ["landray", "Landray", "蓝凌"],
        "severity": "low",
    },
    # ==== 红帆 / 万户 =======================================================
    {
        "type": "component_exposure",
        "name": "HongFan ioffice fingerprint",
        "paths": ["/hh/", "/default.aspx"],
        "check": "pattern",
        "patterns": ["红帆", "ioffice", "hhsoft"],
        "severity": "low",
    },
    {
        "type": "component_exposure",
        "name": "Wanhu ezOFFICE fingerprint",
        "paths": ["/default/html/index.jsp"],
        "check": "pattern",
        "patterns": ["万户", "ezOFFICE", "ezoffice"],
        "severity": "low",
    },
]


def probe_cn_components(targets: list[str]) -> list[dict]:
    """Run all CN component probes against every target.

    Reuses quick_combat._run_quick_probe (lazy import avoids a circular
    dependency: quick_combat imports this module at pipeline time).

    Returns finding dicts in the standard pipeline shape. Any per-probe
    error is swallowed (never aborts the batch).
    """
    import quick_combat as qc

    findings: list[dict] = []
    for target in targets:
        for probe in CN_PROBES:
            try:
                findings.extend(qc._run_quick_probe(target, probe))
            except Exception:
                continue
    return findings


def main() -> int:
    ap = argparse.ArgumentParser(description="CN Component Probes v1.0")
    ap.add_argument("--targets", required=True,
                    help="Targets: comma-separated URLs, JSON file, or text file")
    args = ap.parse_args()

    from quick_combat import _load_targets
    targets = _load_targets(args.targets)
    if not targets:
        print("[!] No targets loaded", file=sys.stderr)
        return 2

    findings = probe_cn_components(targets)
    print(dump_json({
        "tool": "cn_probes",
        "version": "1.0.0",
        "targets": targets,
        "total_findings": len(findings),
        "findings": findings,
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
