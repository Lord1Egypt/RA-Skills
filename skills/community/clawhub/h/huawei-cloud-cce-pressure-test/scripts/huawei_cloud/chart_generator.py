"""监控图表 & 诊断报告生成器

支持两种输出模式：
1. 监控看板 (generate_monitor_dashboard) - 纯监控数据展示
2. 诊断报告 (generate_diagnosis_report) - 完整 7 步诊断报告，内嵌监控图表

Chart.js 和 date-fns adapter 全部内联，无需外部 CDN 依赖。

典型用法:
    # 监控看板
    from huawei_cloud.chart_generator import generate_monitor_dashboard
    result = generate_monitor_dashboard(
        region='cn-north-4',
        cluster_id='034b98c7-1c4d-11f1-842d-0255ac100249',
        namespace='default',
        label_selector='app=nginx',
        hours=1,
    )

    # 诊断报告
    from huawei_cloud.chart_generator import generate_diagnosis_report
    result = generate_diagnosis_report(
        region='cn-north-4',
        cluster_id='034b98c7-1c4d-11f1-842d-0255ac100249',
        workload_name='nginx',
        namespace='default',
    )
"""

from __future__ import annotations

import json
import os
import time as time_module
from typing import Any, Dict, List, Optional

from .common import get_credentials_with_region
from . import aom, cce
from .cce_metrics import get_cce_pod_metrics_topN
from .cce_diagnosis import get_aom_instance

# ─── Chart.js source (bundled) ───────────────────────────────────────────
_chart_js_src: Optional[str] = None
_adapter_js_src: Optional[str] = None


def _load_bundled_js() -> tuple[str, str]:
    """Load Chart.js and date-fns adapter from bundled files."""
    global _chart_js_src, _adapter_js_src
    if _chart_js_src is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        chart_path = os.path.join(base_dir, '_vendor', 'chart.umd.min.js')
        adapter_path = os.path.join(base_dir, '_vendor', 'chartjs-adapter-date-fns.bundle.min.js')
        try:
            with open(chart_path, 'r', encoding='utf-8') as f:
                _chart_js_src = f.read()
        except FileNotFoundError:
            _chart_js_src = ''
        try:
            with open(adapter_path, 'r', encoding='utf-8') as f:
                _adapter_js_src = f.read()
        except FileNotFoundError:
            _adapter_js_src = ''
    return _chart_js_src, _adapter_js_src


# ─── Data Collection ──────────────────────────────────────────────────────

def collect_metrics(
    region: str,
    cluster_id: str,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
    namespace: Optional[str] = None,
    label_selector: Optional[str] = None,
    hours: int = 1,
    include_network: bool = True,
    top_n: int = 10,
) -> Dict[str, Any]:
    """采集 CCE 工作负载的 CPU、内存、网络监控数据。"""
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)

    # CPU and Memory via cce_metrics
    metrics_result = get_cce_pod_metrics_topN(
        region=region, cluster_id=cluster_id,
        ak=access_key, sk=secret_key, project_id=proj_id,
        namespace=namespace, label_selector=label_selector,
        top_n=top_n, hours=hours,
    )

    cpu_data: Dict[str, List] = {}
    memory_data: Dict[str, List] = {}

    if metrics_result.get("success"):
        for item in metrics_result.get("metrics", {}).get("cpu_top_n", []):
            pod_full = item.get("pod", "unknown")
            pod_label = _shorten_pod_name(pod_full)
            ts = item.get("time_series", [])
            cpu_data[pod_label] = [[t[0], round(float(t[1]), 2)] for t in ts]

        for item in metrics_result.get("metrics", {}).get("memory_top_n", []):
            pod_full = item.get("pod", "unknown")
            pod_label = _shorten_pod_name(pod_full)
            ts = item.get("time_series", [])
            memory_data[pod_label] = [[t[0], round(float(t[1]), 2)] for t in ts]

    # Network via AOM PromQL
    net_data: Dict[str, Dict[str, List]] = {}

    if include_network:
        aom_result = get_aom_instance(region, cluster_id, access_key, secret_key, proj_id)
        if aom_result.get("success"):
            aom_instance_id = aom_result.get("aom_instance_id")
            ns_filter = f',namespace="{namespace}"' if namespace else ""

            # Build pod regex from found pods
            pod_names = [item.get("pod", "") for item in metrics_result.get("metrics", {}).get("cpu_top_n", [])]
            if not pod_names:
                # If no pods found via CPU metrics, use wildcard for the namespace
                pod_re = ".*"
            else:
                pod_re = "|".join(pod_names[:50])

            ns_value = namespace if namespace else ".*"
            queries = {
                "rx": f'sum by (pod) (rate(container_network_receive_bytes_total{{namespace="{ns_value}",pod=~"{pod_re}"}}[5m]))',
                "tx": f'sum by (pod) (rate(container_network_transmit_bytes_total{{namespace="{ns_value}",pod=~"{pod_re}"}}[5m]))',
            }

            for direction, query in queries.items():
                try:
                    result = aom.get_aom_prom_metrics_http(
                        region=region, aom_instance_id=aom_instance_id,
                        query=query, hours=hours, step=60,
                        ak=access_key, sk=secret_key, project_id=proj_id,
                    )
                    series_list = result.get("result", {}).get("data", {}).get("result", [])
                    for s in series_list:
                        pod_full = s.get("metric", {}).get("pod", "?")
                        pod_label = _shorten_pod_name(pod_full)
                        vals = s.get("values", [])
                        net_data.setdefault(pod_label, {})[direction] = [
                            [v[0], round(float(v[1]) / 1024, 2)] for v in vals
                        ]
                except Exception:
                    pass

    return {"cpu": cpu_data, "memory": memory_data, "network": net_data}


def _shorten_pod_name(pod_name: str) -> str:
    parts = pod_name.split("-")
    if len(parts) >= 3 and len(parts[-1]) <= 6 and len(parts[-2]) <= 10:
        return parts[-1]
    return pod_name


# ─── HTML Generation ───────────────────────────────────────────────────────

# Template uses 【bracket】 placeholders to avoid f-string / JS brace conflicts
_HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>【title】</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f0f1a;color:#e0e0f0;font-family:'Segoe UI',system-ui,-apple-system,sans-serif;min-height:100vh}
.container{max-width:1200px;margin:0 auto;padding:24px 20px}
.header{text-align:center;margin-bottom:28px}
.header h1{font-size:24px;font-weight:700;color:#fff;letter-spacing:.5px}
.header h1 span{color:#6c8cff}
.header .sub{color:#8888aa;font-size:13px;margin-top:6px}
.stats-row{display:flex;gap:12px;margin-bottom:24px;flex-wrap:wrap}
.stat-card{flex:1;min-width:140px;background:linear-gradient(135deg,#1a1a30,#1e1e38);border:1px solid #2a2a4a;border-radius:12px;padding:16px 18px}
.stat-card .label{font-size:11px;color:#8888aa;text-transform:uppercase;letter-spacing:1px}
.stat-card .value{font-size:26px;font-weight:700;margin-top:4px}
.stat-card .value.green{color:#4ade80}
.stat-card .value.blue{color:#60a5fa}
.stat-card .value.yellow{color:#fbbf24}
.stat-card .value.purple{color:#a78bfa}
.stat-card .detail{font-size:11px;color:#666688;margin-top:2px}
.chart-wrapper{background:linear-gradient(135deg,#1a1a30,#1e1e38);border:1px solid #2a2a4a;border-radius:14px;padding:20px 20px 12px;margin-bottom:20px}
.chart-title{font-size:15px;font-weight:600;margin-bottom:12px;display:flex;align-items:center;gap:8px}
.chart-title .icon{font-size:18px}
.chart-box{position:relative;height:280px;width:100%}
.chart-box canvas{position:absolute;top:0;left:0;width:100%!important;height:100%!important}
.footer{text-align:center;color:#555577;font-size:11px;margin-top:16px}
.err{color:#ff6b6b;background:#2a1a1a;border:1px solid #4a2a2a;border-radius:8px;padding:12px;margin:8px 0;font-size:13px;white-space:pre-wrap;display:none}
@media(max-width:600px){.stats-row{flex-direction:column}.container{padding:16px 10px}}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>📊 <span>【title】</span></h1>
    <div class="sub" id="timeRange">集群 【cluster_name】 · 【region】</div>
  </div>
  <div id="errBox" class="err"></div>
  <div class="stats-row" id="statsRow"></div>
  <div class="chart-wrapper">
    <div class="chart-title"><span class="icon">⚡</span> CPU 使用率 (%)</div>
    <div class="chart-box"><canvas id="cpuChart"></canvas></div>
  </div>
【memory_section】
【network_section】
【extra_sections】
  <div class="footer">OpenClaw · 助手1号 🫡 自动生成 · 【gen_time】</div>
</div>
【chart_tag】
【adapter_tag】
<script>
try{
var DATA = 【metrics_json】;
var EXTRA = 【extra_json】;
var TZ = 【tz_offset】;

var COLORS=['#ef4444','#3b82f6','#22c55e','#f59e0b','#a855f7'];
var COLORS_A=['rgba(239,68,68,.12)','rgba(59,130,246,.12)','rgba(34,197,94,.12)','rgba(245,158,11,.12)','rgba(168,85,247,.12)'];

function ts2d(ts){return new Date(ts*1000+TZ*3600000)}
function fmtT(ts){var d=ts2d(ts);return String(d.getUTCHours()).padStart(2,'0')+':'+String(d.getUTCMinutes()).padStart(2,'0')}

var pods=Object.keys(DATA.cpu).sort();
var tCpu=0,tMem=0,tRx=0,tTx=0;
pods.forEach(function(p){
  var v=DATA.cpu[p].map(function(x){return x[1]});var a=v.reduce(function(s,x){return s+x},0)/v.length;tCpu+=a;
  if(DATA.memory&&DATA.memory[p]){var m=DATA.memory[p].map(function(x){return x[1]});tMem+=m.reduce(function(s,x){return s+x},0)/m.length}
  if(DATA.network[p]){
    if(DATA.network[p].rx){var r=DATA.network[p].rx.map(function(x){return x[1]});tRx+=r.reduce(function(s,x){return s+x},0)/r.length}
    if(DATA.network[p].tx){var t=DATA.network[p].tx.map(function(x){return x[1]});tTx+=t.reduce(function(s,x){return s+x},0)/t.length}
  }
});
var cpuMx=Math.max.apply(null,pods.flatMap(function(p){return DATA.cpu[p].map(function(x){return x[1]})}));
var rxMx=Math.max.apply(null,pods.flatMap(function(p){return(DATA.network[p]&&DATA.network[p].rx)?DATA.network[p].rx.map(function(x){return x[1]}):[0]}));
var txMx=Math.max.apply(null,pods.flatMap(function(p){return(DATA.network[p]&&DATA.network[p].tx)?DATA.network[p].tx.map(function(x){return x[1]}):[0]}));

var statsHtml='<div class="stat-card"><div class="label">平均 CPU</div><div class="value green">'+(tCpu/pods.length).toFixed(1)+'%</div><div class="detail">峰值 '+cpuMx.toFixed(1)+'%</div></div>';
if(tMem>0)statsHtml+='<div class="stat-card"><div class="label">平均内存</div><div class="value blue">'+(tMem/pods.length).toFixed(2)+'%</div><div class="detail">'+pods.length+' Pods</div></div>';
if(tRx>0)statsHtml+='<div class="stat-card"><div class="label">总入站流量</div><div class="value yellow">'+tRx.toFixed(0)+' KB/s</div><div class="detail">峰值 '+rxMx.toFixed(0)+' KB/s</div></div>';
if(tTx>0)statsHtml+='<div class="stat-card"><div class="label">总出站流量</div><div class="value purple">'+tTx.toFixed(0)+' KB/s</div><div class="detail">峰值 '+txMx.toFixed(0)+' KB/s</div></div>';
document.getElementById('statsRow').innerHTML=statsHtml;

var allT=pods.flatMap(function(p){return DATA.cpu[p].map(function(x){return x[0]})});
if(allT.length)document.getElementById('timeRange').textContent+=' · '+fmtT(Math.min.apply(null,allT))+' ~ '+fmtT(Math.max.apply(null,allT));

Chart.defaults.color='#8888aa';
Chart.defaults.borderColor='rgba(255,255,255,.06)';
Chart.defaults.font.family="'Segoe UI',system-ui,sans-serif";

function mkDS(src,pods,opts){
  opts=opts||{};
  return pods.map(function(p,i){
    return {label:p,data:src[p].map(function(v){return{x:ts2d(v[0]),y:v[1]}}),
    borderColor:COLORS[i],backgroundColor:opts.fill?COLORS_A[i]:'transparent',fill:!!opts.fill,
    tension:.3,pointRadius:0,pointHoverRadius:4,borderWidth:2,borderDash:opts.dash||[]};
  });
}

var sc={x:{type:'time',time:{tooltipFormat:'HH:mm',displayFormats:{minute:'HH:mm'}},grid:{color:'rgba(255,255,255,.04)'},ticks:{font:{size:11}}},
  y:{grid:{color:'rgba(255,255,255,.04)'},ticks:{font:{size:11}},beginAtZero:true}};
var ttOpts={backgroundColor:'rgba(15,15,30,.95)',titleFont:{size:12},bodyFont:{size:11},padding:10,cornerRadius:8};
var legOpts={labels:{usePointStyle:true,pointStyle:'circle',padding:16,font:{size:11}}};

// CPU chart
new Chart(document.getElementById('cpuChart'),{type:'line',data:{datasets:mkDS(DATA.cpu,pods,{fill:true})},
  options:{responsive:true,maintainAspectRatio:false,interaction:{intersect:false,mode:'index'},scales:sc,
    plugins:{legend:legOpts,tooltip:Object.assign({},ttOpts,{callbacks:{label:function(c){return c.dataset.label+': '+c.parsed.y.toFixed(2)+'%'}}})}}});

// Memory chart
if(DATA.memory&&Object.keys(DATA.memory).length)
  new Chart(document.getElementById('memChart'),{type:'line',data:{datasets:mkDS(DATA.memory,pods,{fill:true})},
    options:{responsive:true,maintainAspectRatio:false,interaction:{intersect:false,mode:'index'},scales:sc,
      plugins:{legend:legOpts,tooltip:Object.assign({},ttOpts,{callbacks:{label:function(c){return c.dataset.label+': '+c.parsed.y.toFixed(2)+'%'}}})}}});

// Network chart
【network_js】

// Extra custom charts
【extra_chart_js】

}catch(e){
  document.getElementById('errBox').style.display='block';
  document.getElementById('errBox').textContent='Error: '+e.message+'\\n'+e.stack;
}
</script>
</body>
</html>"""

_NETWORK_SECTION_HTML = """
  <div class="chart-wrapper">
    <div class="chart-title"><span class="icon">📡</span> 网络流量 (KB/s) — 实线入站↓ 虚线出站↑</div>
    <div class="chart-box"><canvas id="netChart"></canvas></div>
  </div>"""

_MEMORY_SECTION_HTML = """
  <div class="chart-wrapper">
    <div class="chart-title"><span class="icon">🧠</span> 内存使用率 (%)</div>
    <div class="chart-box"><canvas id="memChart"></canvas></div>
  </div>"""

_NETWORK_JS = """
var nds=[];
pods.forEach(function(p,i){
  if(DATA.network[p]&&DATA.network[p].rx)
    nds.push({label:p+' ↓入站',data:DATA.network[p].rx.map(function(v){return{x:ts2d(v[0]),y:v[1]}}),
      borderColor:COLORS[i],backgroundColor:COLORS_A[i],fill:true,tension:.3,pointRadius:0,pointHoverRadius:4,borderWidth:2});
  if(DATA.network[p]&&DATA.network[p].tx)
    nds.push({label:p+' ↑出站',data:DATA.network[p].tx.map(function(v){return{x:ts2d(v[0]),y:v[1]}}),
      borderColor:COLORS[i],backgroundColor:'transparent',fill:false,tension:.3,pointRadius:0,pointHoverRadius:4,borderWidth:1.5,borderDash:[6,3]});
});
if(nds.length)
  new Chart(document.getElementById('netChart'),{type:'line',data:{datasets:nds},
    options:{responsive:true,maintainAspectRatio:false,interaction:{intersect:false,mode:'index'},scales:sc,
      plugins:{legend:{labels:{usePointStyle:true,pointStyle:'circle',padding:12,font:{size:10}}},
        tooltip:Object.assign({},ttOpts,{callbacks:{label:function(c){return c.dataset.label+': '+c.parsed.y.toFixed(1)+' KB/s'}}})}}});
"""


def _render_html(
    title: str,
    cluster_name: str,
    region: str,
    metrics: Dict[str, Any],
    extra_metrics: Dict[str, Dict[str, List]],
    include_network: bool,
    tz_offset_hours: int,
    inline_js: bool,
) -> str:
    """Render the full HTML dashboard using placeholder substitution."""

    metrics_json = json.dumps(metrics, separators=(',', ':'))
    extra_json = json.dumps(extra_metrics, separators=(',', ':'))

    # Load JS
    if inline_js:
        chart_js, adapter_js = _load_bundled_js()
        chart_tag = f'<script>{chart_js}</script>'
        adapter_tag = f'<script>{adapter_js}</script>'
    else:
        chart_tag = '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>'
        adapter_tag = '<script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns@3.0.0/dist/chartjs-adapter-date-fns.bundle.min.js"></script>'

    # Sections
    memory_section = _MEMORY_SECTION_HTML if metrics.get("memory") else ""
    network_section = _NETWORK_SECTION_HTML if include_network else ""
    network_js = _NETWORK_JS if include_network else ""

    # Extra chart sections
    extra_sections = ""
    extra_chart_js = ""
    for chart_name, series_data in extra_metrics.items():
        chart_id = chart_name.replace(" ", "_").replace("/", "_").lower()
        extra_sections += f'\n  <div class="chart-wrapper">\n    <div class="chart-title"><span class="icon">📈</span> {chart_name}</div>\n    <div class="chart-box"><canvas id="extra_{chart_id}"></canvas></div>\n  </div>'

        colors_js = "['#ef4444','#3b82f6','#22c55e','#f59e0b','#a855f7','#ec4899','#14b8a6','#f97316','#8b5cf6','#06b6d4']"
        colors_a_js = "['rgba(239,68,68,.12)','rgba(59,130,246,.12)','rgba(34,197,94,.12)','rgba(245,158,11,.12)','rgba(168,85,247,.12)','rgba(236,72,153,.12)','rgba(20,184,166,.12)','rgba(249,115,22,.12)','rgba(139,92,246,.12)','rgba(6,182,212,.12)']"
        extra_chart_js += f"""
(function(){{
  var ed=EXTRA["{chart_name}"];
  if(!ed||!Object.keys(ed).length)return;
  var labels=Object.keys(ed);var cs={colors_js};var ca={colors_a_js};
  var ds=labels.map(function(k,i){{return{{label:k,data:ed[k].map(function(v){{return{{x:ts2d(v[0]),y:v[1]}}}}),
    borderColor:cs[i%cs.length],backgroundColor:ca[i%ca.length],fill:true,tension:.3,pointRadius:0,pointHoverRadius:4,borderWidth:2}}}});
  new Chart(document.getElementById("extra_{chart_id}"),{{type:"line",data:{{datasets:ds}},
    options:{{responsive:true,maintainAspectRatio:false,interaction:{{intersect:false,mode:"index"}},scales:sc,
      plugins:{{legend:legOpts,tooltip:Object.assign({{}},ttOpts)}}}}}});
}})();
"""

    gen_time = time_module.strftime('%Y-%m-%d %H:%M', time_module.localtime())

    # Substitute placeholders
    html = _HTML_TEMPLATE
    html = html.replace('【title】', title)
    html = html.replace('【cluster_name】', cluster_name)
    html = html.replace('【region】', region)
    html = html.replace('【gen_time】', gen_time)
    html = html.replace('【metrics_json】', metrics_json)
    html = html.replace('【extra_json】', extra_json)
    html = html.replace('【tz_offset】', str(tz_offset_hours))
    html = html.replace('【chart_tag】', chart_tag)
    html = html.replace('【adapter_tag】', adapter_tag)
    html = html.replace('【memory_section】', memory_section)
    html = html.replace('【network_section】', network_section)
    html = html.replace('【network_js】', network_js)
    html = html.replace('【extra_sections】', extra_sections)
    html = html.replace('【extra_chart_js】', extra_chart_js)

    return html


# ─── Main API ────────────────────────────────────────────────────────────────

def generate_monitor_dashboard(
    region: str,
    cluster_id: str,
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
    namespace: Optional[str] = None,
    label_selector: Optional[str] = None,
    hours: int = 1,
    include_network: bool = True,
    top_n: int = 10,
    output_file: Optional[str] = None,
    title: Optional[str] = None,
    tz_offset_hours: int = 8,
    inline_js: bool = True,
    extra_promql: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    """生成 CCE 工作负载监控 HTML 看板。

    自动采集 CPU/内存/网络数据，生成自包含的 HTML 文件，无需外部 CDN。

    Args:
        region: 华为云区域 (如 cn-north-4)
        cluster_id: CCE 集群 ID
        ak: Access Key ID (可选)
        sk: Secret Access Key (可选)
        project_id: 项目 ID (可选)
        namespace: 命名空间 (可选)
        label_selector: 标签选择器，如 "app=nginx" (可选)
        hours: 查询时间范围（小时），默认 1
        include_network: 是否包含网络流量图表，默认 True
        top_n: 返回 Top N Pod 数量，默认 10
        output_file: 输出 HTML 文件路径，默认 /tmp/cce_monitor_<cluster>.html
        title: 看板标题，默认根据 label_selector 自动生成
        tz_offset_hours: 时区偏移（小时），默认 8 (UTC+8)
        inline_js: 是否内联 Chart.js (推荐 True，避免 CDN 不可用)
        extra_promql: 额外的自定义 PromQL 查询，格式 {"图表名": "promql表达式"}

    Returns:
        Dict with success, output_file, and data summary
    """
    start_time = time_module.time()

    # Get cluster name for title
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)
    cluster_name = cluster_id
    try:
        clusters_result = cce.list_cce_clusters(region, access_key, secret_key, proj_id)
        if clusters_result.get("success"):
            for c in clusters_result.get("clusters", []):
                if c.get("id") == cluster_id:
                    cluster_name = c.get("name", cluster_id)
                    break
    except Exception:
        pass

    # Generate default title
    if title is None:
        if label_selector:
            app_name = label_selector.split("=")[-1] if "=" in label_selector else label_selector
            title = f"{app_name} 监控看板"
        elif namespace:
            title = f"{namespace} 命名空间监控看板"
        else:
            title = "CCE 集群监控看板"

    # Collect metrics
    try:
        metrics = collect_metrics(
            region=region, cluster_id=cluster_id,
            ak=ak, sk=sk, project_id=project_id,
            namespace=namespace, label_selector=label_selector,
            hours=hours, include_network=include_network, top_n=top_n,
        )
    except Exception as exc:
        return {"success": False, "error": f"采集监控数据失败: {exc}"}

    # Collect extra PromQL if provided
    extra_metrics: Dict[str, Dict[str, List]] = {}
    if extra_promql:
        aom_result = get_aom_instance(region, cluster_id, access_key, secret_key, proj_id)
        if aom_result.get("success"):
            aom_instance_id = aom_result.get("aom_instance_id")
            for chart_name, query in extra_promql.items():
                try:
                    result = aom.get_aom_prom_metrics_http(
                        region=region, aom_instance_id=aom_instance_id,
                        query=query, hours=hours, step=60,
                        ak=access_key, sk=secret_key, project_id=proj_id,
                    )
                    series_data: Dict[str, List] = {}
                    series_list = result.get("result", {}).get("data", {}).get("result", [])
                    for s in series_list:
                        label_parts = []
                        m = s.get("metric", {})
                        for k in ("pod", "instance", "namespace"):
                            if k in m:
                                label_parts.append(m[k])
                        series_label = "/".join(label_parts) or chart_name
                        vals = s.get("values", [])
                        series_data[series_label] = [[v[0], round(float(v[1]), 2)] for v in vals]
                    extra_metrics[chart_name] = series_data
                except Exception:
                    pass

    # Generate HTML
    html = _render_html(
        title=title, cluster_name=cluster_name, region=region,
        metrics=metrics, extra_metrics=extra_metrics,
        include_network=include_network, tz_offset_hours=tz_offset_hours,
        inline_js=inline_js,
    )

    # Output file
    if output_file is None:
        output_file = f"/tmp/cce_monitor_{cluster_id[:8]}.html"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    elapsed = round(time_module.time() - start_time, 1)

    cpu_pods = list(metrics.get("cpu", {}).keys())
    mem_pods = list(metrics.get("memory", {}).keys())
    net_pods = list(metrics.get("network", {}).keys())

    return {
        "success": True,
        "output_file": output_file,
        "file_size_kb": round(len(html.encode("utf-8")) / 1024, 1),
        "generation_time_s": elapsed,
        "cluster_name": cluster_name,
        "cluster_id": cluster_id,
        "title": title,
        "data_summary": {
            "cpu_pods": len(cpu_pods),
            "memory_pods": len(mem_pods),
            "network_pods": len(net_pods),
            "hours": hours,
        },
        "message": f"监控看板已生成: {output_file} ({len(html.encode('utf-8'))//1024}KB, {elapsed}s)",
    }


# ═══════════════════════════════════════════════════════════════════════════
# 诊断报告生成
# ═══════════════════════════════════════════════════════════════════════════

def _build_chart_datasets_js(series_list: List[Dict]) -> str:
    """将监控时序数据转为 Chart.js datasets JS 字符串。时间戳转毫秒，值转 float。"""
    colors = ['#6c8cff', '#4ade80', '#fbbf24', '#f87171', '#a78bfa',
              '#22d3ee', '#fb923c', '#e879f9', '#34d399', '#f472b6']
    datasets = []
    for i, s in enumerate(series_list):
        pod_name = _shorten_pod_name(s.get('pod', f'pod-{i}'))
        ts = s.get('time_series', [])
        points = []
        for t, v in ts:
            t_ms = int(t) * 1000 if int(t) < 1e12 else int(t)
            v_float = float(v)
            points.append(f'{{x:{t_ms},y:{round(v_float,2)}}}')
        data_str = ','.join(points)
        c = colors[i % len(colors)]
        datasets.append(
            f'{{label:"{pod_name}",data:[{data_str}],'
            f'borderColor:"{c}",backgroundColor:"{c}22",'
            f'fill:false,tension:0.3,pointRadius:1,borderWidth:2}}'
        )
    return ','.join(datasets)


def _esc_html(s) -> str:
    """HTML 转义"""
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def _status_badge(status: str) -> str:
    """状态标签"""
    ok = ['Running', 'Ready', 'OK', 'Available', 'Bound', 'Active']
    bad = ['Failed', 'Error', 'Unknown', 'CrashLoopBackOff', 'Pending']
    s = str(status)
    color = '#4ade80' if s in ok else '#ef4444' if s in bad else '#fbbf24'
    return (f'<span style="display:inline-block;padding:2px 10px;border-radius:9999px;'
            f'font-size:12px;font-weight:600;background:{color}20;color:{color}">{_esc_html(s)}</span>')


def _render_step_alarms(alarms: List) -> str:
    if not alarms:
        return '<div class="ok-box">\u2705 近 【hours】 小时内无关联告警，工作负载无 CPU/\u5185\u5b58/\u6d41\u91cf\u76f8\u5173\u544a\u8b66</div>'
    html = '<table><tr><th>\u544a\u8b66\u540d\u79f0</th><th>\u72b6\u6001</th><th>\u7ea7\u522b</th><th>\u63cf\u8ff0</th></tr>'
    for a in alarms:
        html += f'<tr><td>{_esc_html(a.get("alarm_name", a.get("name", "-")))}</td>'
        html += f'<td>{_status_badge(a.get("alarm_status", "-"))}</td>'
        html += f'<td>{_esc_html(a.get("alarm_level", "-"))}</td>'
        html += f'<td>{_esc_html(a.get("alarm_description", a.get("description", "-")))[:100]}</td></tr>'
    html += '</table>'
    return html


def _render_step_workload(diag: Dict) -> str:
    workloads = diag.get('workloads', {})
    workload_name = diag.get('workload_name', '')
    target_pods = [p for p in workloads.get('pods', []) if workload_name in p.get('name', '')]
    if not workload_name:
        target_pods = workloads.get('pods', [])
    total = len(target_pods)
    running = sum(1 for p in target_pods if p.get('status') == 'Running')
    abnormal_pct = (total - running) / total * 100 if total else 0

    _all_str = "\u5168\u90e8"
    html = '<div class="info-grid">'
    html += f'<div class="info-item"><div class="info-label">\u5de5\u4f5c\u8d1f\u8f7d</div><div class="info-value">{_esc_html(workload_name) or _all_str}</div></div>'
    html += f'<div class="info-item"><div class="info-label">\u547d\u540d\u7a7a\u95f4</div><div class="info-value">{_esc_html(diag.get("namespace", ""))}</div></div>'
    html += f'<div class="info-item"><div class="info-label">\u671f\u671b\u526f\u672c</div><div class="info-value">{total}</div></div>'
    html += f'<div class="info-item"><div class="info-label">\u8fd0\u884c\u526f\u672c</div><div class="info-value" style="color:#4ade80">{running}/{total}</div></div>'
    html += f'<div class="info-item"><div class="info-label">\u5f02\u5e38\u6bd4\u4f8b</div><div class="info-value">{abnormal_pct:.0f}%</div></div>'
    html += '</div>'

    if target_pods:
        html += '<table><tr><th>Pod \u540d\u79f0</th><th>\u72b6\u6001</th><th>\u8282\u70b9 IP</th><th>Pod IP</th><th>\u91cd\u542f</th><th>\u5206\u6790</th></tr>'
        for p in target_pods:
            html += f'<tr><td class="mono">{_esc_html(p.get("name", "-"))}</td>'
            html += f'<td>{_status_badge(p.get("status", "-"))}</td>'
            html += f'<td class="mono">{_esc_html(p.get("node_ip", "-"))}</td>'
            html += f'<td class="mono">{_esc_html(p.get("pod_ip", "-"))}</td>'
            html += f'<td>{p.get("restart_count", 0)}</td>'
            analysis = p.get('analysis', {})
            html += f'<td>{_esc_html(analysis.get("reason", "-"))}</td></tr>'
        html += '</table>'
    return html


def _render_step_metrics(diag: Dict, metrics_data: Dict,
                        cpu_ds: str, mem_ds: str, rx_ds: str, tx_ds: str) -> str:
    html = '<div class="info-grid">'
    html += f'<div class="info-item"><div class="info-label">CPU \u91c7\u96c6</div><div class="info-value">{metrics_data.get("cpu_pods", 0)} Pod</div></div>'
    html += f'<div class="info-item"><div class="info-label">\u5185\u5b58\u91c7\u96c6</div><div class="info-value">{metrics_data.get("memory_pods", 0)} Pod</div></div>'
    html += f'<div class="info-item"><div class="info-label">\u7f51\u7edc\u91c7\u96c6</div><div class="info-value">{metrics_data.get("network_pods", 0)} Pod</div></div>'
    html += '</div>'
    html += '<div class="charts-area">'
    html += '<div class="chart-wrapper"><div class="chart-title">CPU \u4f7f\u7528\u7387 (%)</div><div style="position:relative;height:260px"><canvas id="cpuChart"></canvas></div></div>'
    html += '<div class="chart-wrapper"><div class="chart-title">\u5185\u5b58\u4f7f\u7528\u7387 (%)</div><div style="position:relative;height:260px"><canvas id="memChart"></canvas></div></div>'
    html += '<div class="chart-wrapper"><div class="chart-title">\u7f51\u7edc\u63a5\u6536 (KB/s)</div><div style="position:relative;height:260px"><canvas id="rxChart"></canvas></div></div>'
    html += '<div class="chart-wrapper"><div class="chart-title">\u7f51\u7edc\u53d1\u9001 (KB/s)</div><div style="position:relative;height:260px"><canvas id="txChart"></canvas></div></div>'
    html += '</div>'
    return html


def _render_step_abnormal_pods(diag: Dict) -> str:
    abnormal = diag.get('abnormal_pods', [])
    abnormal_total = diag.get('abnormal_pods_total', len(abnormal))
    if abnormal_total == 0:
        return '<div class="ok-box">\u2705 \u6240\u6709 Pod \u72b6\u6001\u6b63\u5e38\uff0c\u65e0\u91cd\u542f\uff0c\u65e0\u9700\u8be6\u7ec6\u8bca\u65ad</div>'
    html = f'<div class="warn-box">\u26a0\ufe0f \u53d1\u73b0 {abnormal_total} \u4e2a\u5f02\u5e38 Pod\uff08\u6700\u591a\u5c55\u793a 3 \u4e2a\u8be6\u7ec6\u8bca\u65ad\uff09</div>'
    for p in abnormal[:3]:
        html += '<div class="abnormal-pod-card">'
        html += f'<div class="abnormal-pod-header">{_esc_html(p.get("name", "-"))} {_status_badge(p.get("status", "-"))}</div>'
        analysis = p.get('analysis', {})
        html += f'<div class="abnormal-pod-detail"><b>\u5206\u6790:</b> {_esc_html(analysis.get("reason", "-"))}</div>'
        for event in p.get('events', [])[-5:]:
            html += f'<div class="abnormal-pod-detail"><b>\u4e8b\u4ef6:</b> [{_esc_html(event.get("type",""))}] {_esc_html(event.get("reason",""))}: {_esc_html(event.get("message",""))[:100]}</div>'
        html += '</div>'
    return html


def _render_step_nodes(diag: Dict) -> str:
    node_diag = diag.get('node_diagnosis', {})
    if not node_diag.get('success'):
        return '<div class="ok-box">\u2705 \u8282\u70b9\u72b6\u6001\u6b63\u5e38</div>'
    node_details = node_diag.get('details', {}).get('diagnoses', [])
    if not node_details:
        return '<div class="ok-box">\u2705 \u8282\u70b9\u8bca\u65ad\u5b8c\u6210\uff0c\u65e0\u5f02\u5e38\u8282\u70b9</div>'
    html = f'<div class="info-box">\u8bca\u65ad\u4e86 {len(node_details)} \u4e2a\u8282\u70b9</div>'
    html += '<table><tr><th>\u8282\u70b9 IP</th><th>CPU</th><th>\u5185\u5b58</th><th>\u78c1\u76d8</th><th>\u5de5\u4f5c\u8d1f\u8f7d\u6570</th></tr>'
    for nd in node_details:
        m = nd.get('monitoring', {})
        cpu_val = m.get('cpu', '-')
        mem_val = m.get('memory', '-')
        disk_val = m.get('disk', '-')
        cpu_c = '#ef4444' if isinstance(cpu_val, (int, float)) and cpu_val > 80 else '#4ade80'
        mem_c = '#ef4444' if isinstance(mem_val, (int, float)) and mem_val > 80 else '#4ade80'
        html += f'<tr><td class="mono">{_esc_html(nd.get("node_ip", "-"))}</td>'
        html += f'<td style="color:{cpu_c}">{cpu_val}%</td>'
        html += f'<td style="color:{mem_c}">{mem_val}%</td>'
        html += f'<td>{disk_val}%</td>'
        html += f'<td>{len(nd.get("workloads", []))}</td></tr>'
    html += '</table>'
    abnormal_nodes = node_diag.get('abnormal_nodes', [])
    if abnormal_nodes:
        html += f'<div class="warn-box">\u26a0\ufe0f \u5f02\u5e38\u8282\u70b9: {", ".join(_esc_html(n) for n in abnormal_nodes)}</div>'
    return html


def _render_step_network(diag: Dict) -> str:
    net_diag = diag.get('network_diagnosis', {})
    if not net_diag.get('success') or not net_diag.get('chain'):
        return '<div class="ok-box">\u2705 \u7f51\u7edc\u94fe\u8def\u6b63\u5e38</div>'
    chain = net_diag['chain']
    items = [('\U0001f310 \u5916\u90e8\u6d41\u91cf', True)]
    if chain.get('eip'):
        items.append((f'EIP: {_esc_html(chain["eip"].get("ip_address", "-"))}', True))
    elb_list = chain.get('elb', [])
    if isinstance(elb_list, dict):
        elb_list = [elb_list]
    for elb in elb_list:
        items.append((f'ELB: {_esc_html(elb.get("name", elb.get("id", "-")[:8]))}', True))
    if chain.get('nat') and chain['nat'].get('count', 0) > 0:
        items.append(('NAT Gateway', True))
    if chain.get('ingress'):
        items.append((f'Ingress: {_esc_html(chain["ingress"].get("name", "-"))}', True))
    svc = chain.get('service')
    if svc:
        items.append((f'Service: {_esc_html(svc.get("name", "-"))} ({_esc_html(svc.get("type", "ClusterIP"))})', True))
    else:
        items.append(('Service: \u672a\u53d1\u73b0', False))
    pods = chain.get('pods', [])
    items.append((f'Pods ({len(pods)})', len(pods) > 0))
    nodes = chain.get('nodes', [])
    if nodes:
        items.append((f'\u8282\u70b9 ({len(nodes)})', True))
    html = '<div class="chain-flow">'
    for i, (label, ok) in enumerate(items):
        c = '#4ade80' if ok else '#ef4444'
        html += f'<div class="chain-node" style="border-color:{c}"><span style="color:{c}">\u25cf</span> {label}</div>'
        if i < len(items) - 1:
            html += '<div class="chain-arrow">\u2192</div>'
    html += '</div>'
    if svc:
        html += '<div class="info-grid">'
        html += f'<div class="info-item"><div class="info-label">Service</div><div class="info-value">{_esc_html(svc.get("name","-"))}</div></div>'
        html += f'<div class="info-item"><div class="info-label">\u7c7b\u578b</div><div class="info-value">{_esc_html(svc.get("type","ClusterIP"))}</div></div>'
        html += f'<div class="info-item"><div class="info-label">ClusterIP</div><div class="info-value mono">{_esc_html(svc.get("cluster_ip","-"))}</div></div>'
        html += '</div>'
    for elb in elb_list:
        html += '<div class="info-grid">'
        html += f'<div class="info-item"><div class="info-label">ELB</div><div class="info-value">{_esc_html(elb.get("name", elb.get("id","-")[:8]))}</div></div>'
        html += f'<div class="info-item"><div class="info-label">\u5185\u7f51 IP</div><div class="info-value mono">{_esc_html(elb.get("private_ip", "-"))}</div></div>'
        html += '</div>'
    analysis = net_diag.get('analysis', {})
    issues = []
    for comp in ['elb', 'eip', 'service']:
        if analysis.get(comp, {}).get('status') == 'WARNING':
            issues.append(f'{comp.upper()}: \u5f02\u5e38')
    if issues:
        html += '<div class="warn-box">\u26a0\ufe0f ' + '<br>'.join(_esc_html(i) for i in issues) + '</div>'
    else:
        html += '<div class="ok-box">\u2705 \u7f51\u7edc\u94fe\u8def\u5b8c\u6574\uff0cService \u2192 ELB \u901a\u8def\u6b63\u5e38</div>'
    return html


def _render_step_changes(diag: Dict) -> str:
    change = diag.get('change_correlation', {})
    if change.get('has_correlation'):
        html = '<div class="warn-box">\u26a0\ufe0f \u53d1\u73b0\u76f8\u5173\u53d8\u66f4</div>'
        for c in change.get('changes', [])[:5]:
            html += f'<div class="change-item">{_esc_html(c)}</div>'
        if change.get('analysis'):
            html += f'<div class="info-box">\u5206\u6790: {_esc_html(change["analysis"])}</div>'
        return html
    return '<div class="ok-box">\u2705 \u8fd1 1 \u5c0f\u65f6\u5185\u65e0\u76f8\u5173\u914d\u7f6e\u53d8\u66f4\u6216\u7248\u672c\u66f4\u65b0</div>'


def _render_top3(top3: List[Dict]) -> str:
    if not top3:
        return '<div class="ok-box">\u2705 \u672a\u53d1\u73b0\u5f02\u5e38\u6839\u56e0\uff0c\u5de5\u4f5c\u8d1f\u8f7d\u72b6\u6001\u6b63\u5e38</div>'
    html = ''
    for c in top3:
        conf_color = {'high': '#4ade80', 'medium': '#fbbf24', 'low': '#888'}.get(c.get('confidence', ''), '#888')
        html += f'<div class="root-cause-card"><div class="rc-rank">#{c.get("rank", 1)}</div>'
        html += f'<div class="rc-body"><div class="rc-cat">{_esc_html(c.get("category", ""))}</div>'
        html += f'<div class="rc-cause">{_esc_html(c.get("cause", ""))}</div>'
        html += f'<div class="rc-evidence">\u8bc1\u636e: {_esc_html(c.get("evidence", ""))} \u00b7 \u7f6e\u4fe1\u5ea6: <span style="color:{conf_color}">{_esc_html(c.get("confidence", ""))}</span></div>'
        html += '</div></div>'
    return html


def _render_recommendations(recs: List[Dict]) -> str:
    if not recs:
        return '<div class="ok-box">\u2705 \u6682\u65e0\u6062\u590d\u5efa\u8bae\uff0c\u5de5\u4f5c\u8d1f\u8f7d\u8fd0\u884c\u6b63\u5e38</div>'
    cat_colors = {'CPU\u74f6\u9888': '#ef4444', '\u5185\u5b58\u74f6\u9888': '#f59e0b', '\u544a\u8b66\u5173\u8054\u76d1\u63a7': '#3b82f6'}
    html = ''
    for r in recs:
        cc = cat_colors.get(r.get('category', ''), '#8888aa')
        html += f'<div class="rec-card">'
        html += f'<span class="rec-cat" style="background:{cc}20;color:{cc}">{_esc_html(r.get("category", ""))}</span>'
        html += f'<span class="rec-issue">{_esc_html(r.get("issue", ""))}</span>'
        html += f'<span class="rec-suggestion">\u2192 {_esc_html(r.get("suggestion", ""))}</span>'
        html += '</div>'
    return html


# 诊断报告 HTML 模板 — 使用 \u3010placeholder\u3011 避免与 JS 花括号冲突
_DIAG_REPORT_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>\u3010workload_name\u3011 \u5de5\u4f5c\u8d1f\u8f7d\u8bca\u65ad\u62a5\u544a</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f0f1a;color:#e0e0f0;font-family:'Segoe UI',system-ui,-apple-system,sans-serif;min-height:100vh}
.container{max-width:1100px;margin:0 auto;padding:28px 20px}
.header{text-align:center;margin-bottom:32px}
.header h1{font-size:26px;font-weight:700;color:#fff}
.header h1 span{color:#6c8cff}
.header .sub{color:#8888aa;font-size:13px;margin-top:6px}
.header .time{color:#666688;font-size:12px;margin-top:4px}
.progress{background:#1a1a30;border:1px solid #2a2a4a;border-radius:12px;padding:20px;margin-bottom:28px}
.progress h3{font-size:14px;color:#6c8cff;margin-bottom:14px}
.step-item{display:flex;align-items:center;gap:10px;margin-bottom:8px}
.step-item.done .step-num{background:#4ade80;color:#0f0f1a}
.step-num{width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;background:#2a2a4a;color:#8888aa;flex-shrink:0}
.step-text{font-size:13px;color:#ccccdd}
.section{background:linear-gradient(135deg,#1a1a30,#1e1e38);border:1px solid #2a2a4a;border-radius:14px;padding:22px;margin-bottom:20px}
.section-title{font-size:16px;font-weight:600;margin-bottom:16px;display:flex;align-items:center;gap:8px;color:#fff}
.section-title .icon{font-size:18px}
.info-grid{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px}
.info-item{flex:1;min-width:120px;background:#12122a;border:1px solid #2a2a4a;border-radius:8px;padding:10px 14px}
.info-label{font-size:10px;color:#8888aa;text-transform:uppercase;letter-spacing:.8px}
.info-value{font-size:18px;font-weight:700;margin-top:2px;color:#e0e0f0}
table{width:100%;border-collapse:collapse;margin-top:10px;font-size:13px}
th{text-align:left;padding:8px 10px;background:#12122a;color:#8888aa;font-size:11px;text-transform:uppercase;letter-spacing:.5px;border-bottom:1px solid #2a2a4a}
td{padding:8px 10px;border-bottom:1px solid #1e1e38;color:#ccccdd}
td.mono,.mono{font-family:'SF Mono',Menlo,Consolas,monospace;font-size:12px}
.ok-box{background:#0d2818;border:1px solid #1a4a2a;border-radius:8px;padding:12px 16px;font-size:13px;color:#4ade80}
.warn-box{background:#2a1a0a;border:1px solid #4a2a1a;border-radius:8px;padding:12px 16px;font-size:13px;color:#fbbf24;margin-top:10px}
.info-box{background:#0a1a2a;border:1px solid #1a2a4a;border-radius:8px;padding:12px 16px;font-size:13px;color:#60a5fa}
.empty{color:#666688;font-size:13px;padding:10px}
.chain-flow{display:flex;align-items:center;gap:6px;flex-wrap:wrap;padding:12px 0}
.chain-node{border:1px solid #4ade80;border-radius:8px;padding:6px 14px;font-size:12px;white-space:nowrap}
.chain-arrow{color:#8888aa;font-size:18px}
.abnormal-pod-card{background:#1a1a2a;border:1px solid #3a2a2a;border-radius:10px;padding:14px;margin-top:10px}
.abnormal-pod-header{font-size:14px;font-weight:600;margin-bottom:6px;align-items:center;display:flex;gap:8px}
.abnormal-pod-detail{font-size:13px;color:#ccccdd;margin-top:4px}
.root-cause-card{display:flex;gap:14px;background:#12122a;border:1px solid #2a2a4a;border-radius:10px;padding:14px;margin-bottom:10px}
.rc-rank{font-size:28px;font-weight:800;color:#6c8cff;min-width:40px;text-align:center}
.rc-body{flex:1}
.rc-cat{font-size:11px;text-transform:uppercase;letter-spacing:1px;color:#8888aa}
.rc-cause{font-size:14px;font-weight:600;color:#fff;margin-top:2px}
.rc-evidence{font-size:12px;color:#666688;margin-top:4px}
.rec-card{display:flex;flex-wrap:wrap;gap:8px;align-items:center;background:#12122a;border:1px solid #2a2a4a;border-radius:8px;padding:10px 14px;margin-bottom:8px;font-size:13px}
.rec-cat{padding:2px 8px;border-radius:9999px;font-size:11px;font-weight:600}
.rec-issue{color:#e0e0f0}
.rec-suggestion{color:#4ade80}
.charts-area{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px}
.chart-wrapper{background:#12122a;border:1px solid #2a2a4a;border-radius:10px;padding:14px}
.chart-title{font-size:12px;color:#8888aa;margin-bottom:10px;font-weight:600;text-transform:uppercase;letter-spacing:.5px}
.change-item{background:#12122a;padding:8px 12px;border-radius:6px;margin-bottom:4px;font-size:13px;color:#ccccdd}
.footer{text-align:center;color:#555577;font-size:11px;margin-top:20px;padding:10px}
@media(max-width:700px){.container{padding:14px 10px}.info-grid{flex-direction:column}.chain-flow{flex-direction:column;align-items:flex-start}.charts-area{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>\U0001fa7a <span>\u3010workload_name\u3011</span> \u5de5\u4f5c\u8d1f\u8f7d\u8bca\u65ad\u62a5\u544a</h1>
    <div class="sub">\u96c6\u7fa4 \u3010cluster_name\u3011 \u00b7 \u3010region\u3011 \u00b7 \u547d\u540d\u7a7a\u95f4: \u3010namespace\u3011</div>
    <div class="time">\u751f\u6210\u65f6\u95f4: \u3010gen_time\u3011 \u00b7 \u6570\u636e\u8303\u56f4: \u8fd1 1 \u5c0f\u65f6</div>
  </div>
  <div class="progress">
    <h3>\U0001f4cb \u8bca\u65ad\u6b65\u9aa4 (\u3010steps_done\u3011/7 \u5b8c\u6210)</h3>
    \u3010step_indicator\u3011
  </div>
  <div class="section"><div class="section-title"><span class="icon">\U0001f514</span> \u6b65\u9aa41: AOM \u544a\u8b66\u67e5\u8be2</div>\u3010step1\u3011</div>
  <div class="section"><div class="section-title"><span class="icon">\U0001f4e6</span> \u6b65\u9aa42: \u5de5\u4f5c\u8d1f\u8f7d\u4fe1\u606f</div>\u3010step2\u3011</div>
  <div class="section"><div class="section-title"><span class="icon">\U0001f4ca</span> \u6b65\u9aa43: \u76d1\u63a7\u6570\u636e\u91c7\u96c6</div>\u3010step3\u3011</div>
  <div class="section"><div class="section-title"><span class="icon">\U0001f50d</span> \u6b65\u9aa44: \u5f02\u5e38 Pod \u8bca\u65ad</div>\u3010step4\u3011</div>
  <div class="section"><div class="section-title"><span class="icon">\U0001f5a5\ufe0f</span> \u6b65\u9aa45: \u8282\u70b9\u8bca\u65ad</div>\u3010step5\u3011</div>
  <div class="section"><div class="section-title"><span class="icon">\U0001f310</span> \u6b65\u9aa46: \u7f51\u7edc\u94fe\u8def\u8bca\u65ad</div>\u3010step6\u3011</div>
  <div class="section"><div class="section-title"><span class="icon">\U0001f504</span> \u6b65\u9aa47: \u53d8\u66f4\u5173\u8054\u5206\u6790</div>\u3010step7\u3011</div>
  <div class="section"><div class="section-title"><span class="icon">\U0001f3af</span> Top3 \u6839\u56e0\u5206\u6790</div>\u3010top3\u3011</div>
  <div class="section"><div class="section-title"><span class="icon">\U0001f4a1</span> \u6062\u590d\u5efa\u8bae</div>\u3010recs\u3011</div>
  <div class="footer">OpenClaw \u00b7 \u52a9\u624b1\u53f7 \U0001fae1 \u81ea\u52a8\u8bca\u65ad \u00b7 \u3010gen_time\u3011</div>
</div>
<script>
\u3010chart_js\u3011
\u3010adapter_js\u3011
function makeChart(canvasId, datasets, yLabel, yMax) {
  var ctx = document.getElementById(canvasId);
  if (!ctx) return;
  var yOpts = {};
  if (yMax) yOpts.max = yMax;
  yOpts.beginAtZero = true;
  yOpts.title = {display:true, text:yLabel, color:'#8888aa', font:{size:11}};
  yOpts.ticks = {color:'#666688', font:{size:10}};
  yOpts.grid = {color:'#1e1e38'};
  new Chart(ctx, {
    type: 'line', data: { datasets: datasets },
    options: {
      responsive: true, maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { labels: { color: '#aaaacc', font: { size: 11 }, boxWidth: 12 } },
        tooltip: { backgroundColor: '#1a1a30', titleColor: '#fff', bodyColor: '#ccccdd', borderColor: '#2a2a4a', borderWidth: 1 }
      },
      scales: {
        x: {
          type: 'time',
          time: { displayFormats: { hour: 'HH:mm', minute: 'HH:mm' }, tooltipFormat: 'HH:mm:ss' },
          ticks: { color: '#666688', maxTicksLimit: 8, font: { size: 10 } },
          grid: { color: '#1e1e38' }
        },
        y: yOpts
      }
    }
  });
}
makeChart('cpuChart', [\u3010cpu_ds\u3011], '%', 100);
makeChart('memChart', [\u3010mem_ds\u3011], '%', 100);
makeChart('rxChart', [\u3010rx_ds\u3011], 'KB/s');
makeChart('txChart', [\u3010tx_ds\u3011], 'KB/s');
</script>
</body>
</html>"""


def generate_diagnosis_report(
    region: str,
    cluster_id: str,
    workload_name: str,
    namespace: str = 'default',
    ak: Optional[str] = None,
    sk: Optional[str] = None,
    project_id: Optional[str] = None,
    fault_time: Optional[str] = None,
    hours: int = 6,
    output_file: Optional[str] = None,
) -> Dict[str, Any]:
    """\u751f\u6210\u5305\u542b 7 \u6b65\u5b8c\u6574\u8bca\u65ad\u8fc7\u7a0b\u7684 HTML \u62a5\u544a\uff0c\u76d1\u63a7\u56fe\u8868\u76f4\u63a5\u5185\u5d4c\u3002

    \u6267\u884c workload_diagnose \u83b7\u53d6\u8bca\u65ad\u6570\u636e\uff0c\u91c7\u96c6 CPU/\u5185\u5b58/\u7f51\u7edc\u76d1\u63a7\u65f6\u5e8f\uff0c
    \u751f\u6210\u81ea\u5305\u542b\u7684 HTML \u8bca\u65ad\u62a5\u544a\uff0c\u65e0\u9700\u5916\u90e8 CDN\u3002

    7 \u6b65\u8bca\u65ad\u6d41\u7a0b:
      1. AOM \u544a\u8b66\u67e5\u8be2
      2. \u6536\u96c6\u5de5\u4f5c\u8d1f\u8f7d\u4fe1\u606f
      3. \u6536\u96c6\u76d1\u63a7\u6570\u636e\uff08CPU/\u5185\u5b58/\u7f51\u7edc\u65f6\u5e8f\u56fe\u5185\u5d4c\uff09
      4. \u5f02\u5e38 Pod \u8bca\u65ad\uff08\u6700\u591a 3 \u4e2a\uff09
      5. \u8282\u70b9\u8bca\u65ad
      6. \u7f51\u7edc\u94fe\u8def\u8bca\u65ad
      7. \u53d8\u66f4\u5173\u8054\u5206\u6790

    Args:
        region: \u534e\u4e3a\u4e91\u533a\u57df (\u5982 cn-north-4)
        cluster_id: CCE \u96c6\u7fa4 ID
        workload_name: \u5de5\u4f5c\u8d1f\u8f7d\u540d\u79f0 (\u5982 nginx)
        namespace: \u547d\u540d\u7a7a\u95f4\uff0c\u9ed8\u8ba4 default
        ak: Access Key ID (\u53ef\u9009)
        sk: Secret Access Key (\u53ef\u9009)
        project_id: \u9879\u76ee ID (\u53ef\u9009)
        fault_time: \u6545\u969c\u65f6\u95f4 (\u53ef\u9009)
        hours: \u67e5\u8be2\u65f6\u95f4\u8303\u56f4\uff08\u5c0f\u65f6\uff09\uff0c\u9ed8\u8ba4 1
        output_file: \u8f93\u51fa HTML \u6587\u4ef6\u8def\u5f84\uff0c\u9ed8\u8ba4\u81ea\u52a8\u751f\u6210

    Returns:
        Dict with success, output_file, diagnosis data, etc.
    """
    start_time = time_module.time()
    access_key, secret_key, proj_id = get_credentials_with_region(region, ak, sk, project_id)

    # 1) Run full diagnosis
    from .cce_diagnosis import workload_diagnose
    diag_result = workload_diagnose(
        region=region, cluster_id=cluster_id,
        workload_name=workload_name, namespace=namespace,
        fault_time=fault_time,
        ak=access_key, sk=secret_key, project_id=proj_id,
    )
    if not diag_result.get('success'):
        unknown_err = '\u672a\u77e5\u9519\u8bef'
        return {'success': False, 'error': f'\u8bca\u65ad\u6267\u884c\u5931\u8d25: {diag_result.get("error", unknown_err)}'}

    diag = diag_result.get('diagnosis', {})

    # 2) Collect metrics for inline charts
    metrics_data = diag.get('metrics_data', {})
    cpu_series = []
    mem_series = []
    rx_series = []
    tx_series = []

    try:
        topn_result = get_cce_pod_metrics_topN(
            region=region, cluster_id=cluster_id,
            ak=access_key, sk=secret_key, project_id=proj_id,
            namespace=namespace,
            label_selector=f'app={workload_name}' if workload_name else None,
            top_n=10, hours=hours,
        )
        if topn_result.get('success'):
            cpu_series = topn_result.get('metrics', {}).get('cpu_top_n', [])
            mem_series = topn_result.get('metrics', {}).get('memory_top_n', [])
    except Exception:
        pass

    try:
        aom_result = get_aom_instance(region, cluster_id, access_key, secret_key, proj_id)
        if aom_result.get('success'):
            aom_id = aom_result.get('aom_instance_id')
            ns_val = namespace if namespace else '.*'
            pod_names = [s.get('pod', '') for s in cpu_series]
            pod_re = '|'.join(pod_names[:50]) if pod_names else '.*'

            for direction, field in [('rx', 'receive'), ('tx', 'transmit')]:
                query = (
                    f'sum by (pod) (rate(container_network_{field}_bytes_total'
                    f'{{namespace="{ns_val}",pod=~"{pod_re}"}}[5m]))'
                )
                result = aom.get_aom_prom_metrics_http(
                    region=region, aom_instance_id=aom_id,
                    query=query, hours=hours, step=60,
                    ak=access_key, sk=secret_key, project_id=proj_id,
                )
                series = []
                items = result.get('result', {}).get('data', {}).get('result', [])
                for item in items:
                    pod = item.get('metric', {}).get('pod', 'unknown')
                    vals = item.get('values', [])
                    ts = [[int(v[0]) * 1000, round(float(v[1]) / 1024, 2)] for v in vals]
                    series.append({'pod': pod, 'time_series': ts})
                if direction == 'rx':
                    rx_series = series
                else:
                    tx_series = series
    except Exception:
        pass

    # Build chart datasets
    cpu_ds = _build_chart_datasets_js(cpu_series)
    mem_ds = _build_chart_datasets_js(mem_series)
    rx_ds = _build_chart_datasets_js(rx_series)
    tx_ds = _build_chart_datasets_js(tx_series)

    # 3) Load Chart.js
    chart_js_code, adapter_js_code = _load_bundled_js()

    # 4) Render step sections
    steps = diag.get('steps_completed', [])
    steps_done = len(steps)

    step_indicator_html = ''
    for i, s in enumerate(steps, 1):
        step_indicator_html += f'<div class="step-item done"><div class="step-num">{i}</div><div class="step-text">{_esc_html(s)}</div></div>'

    step1_html = _render_step_alarms(diag.get('alarms', []))
    step2_html = _render_step_workload(diag)
    step3_html = _render_step_metrics(diag, metrics_data, cpu_ds, mem_ds, rx_ds, tx_ds)
    step4_html = _render_step_abnormal_pods(diag)
    step5_html = _render_step_nodes(diag)
    step6_html = _render_step_network(diag)
    step7_html = _render_step_changes(diag)
    top3_html = _render_top3(diag.get('top3_root_causes', []))
    recs_html = _render_recommendations(diag.get('recommendations', []))

    gen_time = time_module.strftime('%Y-%m-%d %H:%M:%S', time_module.localtime())

    # 5) Substitute template placeholders
    html = _DIAG_REPORT_TEMPLATE
    html = html.replace('\u3010workload_name\u3011', _esc_html(workload_name))
    html = html.replace('\u3010cluster_name\u3011', _esc_html(diag.get('cluster_name', cluster_id)))
    html = html.replace('\u3010region\u3011', _esc_html(region))
    html = html.replace('\u3010namespace\u3011', _esc_html(namespace))
    html = html.replace('\u3010gen_time\u3011', gen_time)
    html = html.replace('\u3010hours\u3011', str(hours))
    html = html.replace('\u3010steps_done\u3011', str(steps_done))
    html = html.replace('\u3010step_indicator\u3011', step_indicator_html)
    html = html.replace('\u3010step1\u3011', step1_html)
    html = html.replace('\u3010step2\u3011', step2_html)
    html = html.replace('\u3010step3\u3011', step3_html)
    html = html.replace('\u3010step4\u3011', step4_html)
    html = html.replace('\u3010step5\u3011', step5_html)
    html = html.replace('\u3010step6\u3011', step6_html)
    html = html.replace('\u3010step7\u3011', step7_html)
    html = html.replace('\u3010top3\u3011', top3_html)
    html = html.replace('\u3010recs\u3011', recs_html)
    html = html.replace('\u3010chart_js\u3011', chart_js_code)
    html = html.replace('\u3010adapter_js\u3011', adapter_js_code)
    html = html.replace('\u3010cpu_ds\u3011', cpu_ds)
    html = html.replace('\u3010mem_ds\u3011', mem_ds)
    html = html.replace('\u3010rx_ds\u3011', rx_ds)
    html = html.replace('\u3010tx_ds\u3011', tx_ds)

    # 6) Write output
    if output_file is None:
        output_file = f'/tmp/cce_diag_report_{cluster_id[:8]}_{workload_name}.html'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    elapsed = round(time_module.time() - start_time, 1)

    return {
        'success': True,
        'output_file': output_file,
        'file_size_kb': round(len(html.encode('utf-8')) / 1024, 1),
        'generation_time_s': elapsed,
        'workload_name': workload_name,
        'cluster_id': cluster_id,
        'steps_completed': steps_done,
        'alarms_count': len(diag.get('alarms', [])),
        'abnormal_pods_count': diag.get('abnormal_pods_total', len(diag.get('abnormal_pods', []))),
        'recommendations_count': len(diag.get('recommendations', [])),
        'diagnosis': diag,
        'report': diag_result.get('report', ''),
        'message': f'\u8bca\u65ad\u62a5\u544a\u5df2\u751f\u6210: {output_file} ({round(len(html.encode("utf-8"))/1024)}KB, {elapsed}s)',
    }
