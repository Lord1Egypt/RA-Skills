# -*- coding: utf-8 -*-
import json, os
from datetime import date, timedelta

d = json.load(open('workboard2_data.json', encoding='utf-8'))
CN = json.load(open('workboard2_cn.json', encoding='utf-8')) if os.path.exists('workboard2_cn.json') else {'stores': {}, 'other_todos': {}, 'iberia': {}}
CN_STORES = CN.get('stores', {})
CN_TODOS = CN.get('other_todos', {})
CN_IBERIA = CN.get('iberia', {})

TODAY = d.get('today') or date.today().isoformat()
NEAR30 = (date.fromisoformat(TODAY) - timedelta(days=30)).isoformat()
ME = os.environ.get('MAILBOARD_ME') or 'your-name@company.com'

# augment: monthly aggregation + store counts + dir split
by_month = {}
for dt, cnt in d['by_date'].items():
    if not dt:
        continue
    ym = dt[:7]
    by_month[ym] = by_month.get(ym, 0) + cnt
months = sorted(by_month.keys())
month_data = [{'label': m, 'value': by_month[m]} for m in months]

store_counts = []
for sk in ['Cologne', 'Rome', 'Dusseldorf', 'Zurich']:
    sv = d['stores'][sk]
    store_counts.append({'key': sk, 'label': sv['label'], 'count': sv['emails']})

aug = {
    'volume': d['volume'],
    'months': month_data,
    'store_counts': store_counts,
    'stores': d['stores'],
    'iberia_view': d.get('iberia_view', {'sections': [], 'total': 0, 'monica_count': 0}),
    'reserved': None,
    'other_todos': d['other_todos'],
    'stats': d['stats'],
    'generated_at': d['generated_at'],
    'window': d['window'],
    'today': TODAY,
    'near30_cut': NEAR30,
}

HTML = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>飞书邮件工作看板 · 往来 Summary / 西南欧建店 / 西葡非建店 / 其他事项</title>
<style>
:root{
  --steel:#3E6E9E; --teal:#3E8E80; --ochre:#B5791F; --ink:#2B3440; --sub:#6B7785;
  --line:#E3E8EE; --bg:#F5F7FA; --card:#FFFFFF; --amber:#C2A35A; --purple:#8A7CA8;
}
*{box-sizing:border-box;}
body{margin:0;font-family:"Segoe UI","PingFang SC","Microsoft YaHei",system-ui,sans-serif;background:var(--bg);color:var(--ink);font-size:14px;line-height:1.5;}
.wrap{max-width:1240px;margin:0 auto;padding:20px 20px 50px;}
header.top{background:linear-gradient(135deg,var(--steel),var(--teal));color:#fff;border-radius:14px;padding:18px 24px;box-shadow:0 6px 18px rgba(62,110,158,.18);}
header.top h1{margin:0;font-size:20px;font-weight:700;}
header.top .meta{margin-top:5px;font-size:12px;opacity:.92;}
.tabs{display:flex;gap:6px;margin:14px 0 14px;flex-wrap:wrap;}
.tab{background:var(--card);border:1px solid var(--line);border-radius:9px 9px 0 0;padding:9px 18px;cursor:pointer;font-weight:600;color:var(--sub);font-size:13.5px;}
.tab.active{background:var(--steel);color:#fff;border-color:var(--steel);}
/* 顶部标题区+Tab栏：滚动时固定在视口顶部（像表头一样不动） */
.topbar{position:sticky;top:0;z-index:100;background:var(--bg);box-shadow:0 4px 14px rgba(43,52,64,0.10);}
.topbar header.top{border-radius:0 0 14px 14px;box-shadow:none;}
.topbar .tabs{margin:14px 0 0;}
.panel{display:none;background:var(--card);border:1px solid var(--line);border-radius:0 12px 12px 12px;padding:16px 18px;box-shadow:0 2px 10px rgba(43,52,64,.05);}
.panel.active{display:block;}
.kpis{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px;}
.kpi{background:linear-gradient(135deg,#fff,#F4F8FC);border:1px solid var(--line);border-radius:12px;padding:12px 16px;min-width:120px;flex:1;}
.kpi .n{font-size:24px;font-weight:800;color:var(--steel);}
.kpi .l{font-size:12px;color:var(--sub);margin-top:2px;}
.kpi.t{background:linear-gradient(135deg,#fff,#FBF6EC);} .kpi.t .n{color:var(--ochre);}
.kpi.g{background:linear-gradient(135deg,#fff,#EEF6F2);} .kpi.g .n{color:var(--teal);}
.charts{display:flex;gap:16px;flex-wrap:wrap;}
.chart{background:#FAFCFE;border:1px solid var(--line);border-radius:12px;padding:14px 16px;flex:1;min-width:280px;}
.chart h3{margin:0 0 10px;font-size:13px;color:var(--sub);font-weight:600;}
.bars{display:flex;align-items:flex-end;gap:10px;height:160px;padding-top:8px;}
.bar{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;}
.bar .fill{width:70%;border-radius:6px 6px 0 0;background:var(--steel);min-height:2px;}
.bar .v{font-size:11px;font-weight:700;margin-bottom:3px;color:var(--ink);}
.bar .x{font-size:11px;color:var(--sub);margin-top:5px;white-space:nowrap;}
.toolbar{display:flex;gap:9px;margin-bottom:12px;flex-wrap:wrap;align-items:center;}
.toolbar input,.toolbar select{padding:7px 10px;border:1px solid var(--line);border-radius:8px;font-size:13px;background:#fff;color:var(--ink);}
.toolbar input{flex:1;min-width:160px;}
.toolbar label{font-size:12.5px;color:var(--sub);display:flex;align-items:center;gap:4px;cursor:pointer;}
.toolbar .hint{font-size:12px;color:var(--sub);}
.storebtns{display:flex;gap:8px;margin-bottom:14px;flex-wrap:wrap;}
.sbtn{background:#fff;border:1px solid var(--line);border-radius:9px;padding:8px 14px;cursor:pointer;font-weight:600;color:var(--sub);font-size:13px;}
.sbtn.active{background:var(--steel);color:#fff;border-color:var(--steel);}
.sbtn .c{opacity:.7;font-weight:400;font-size:11px;margin-left:4px;}
.subhead{font-size:15px;font-weight:700;color:var(--steel);margin:14px 0 8px;border-left:3px solid var(--steel);padding-left:8px;}
.storesum{font-size:12.5px;color:var(--sub);margin-bottom:6px;}
.thread{border:1px solid var(--line);border-radius:10px;padding:11px 14px;margin-bottom:10px;background:#FCFDFE;scroll-margin-top:80px;}
.thread .th{font-weight:700;font-size:13.5px;}
.thread .meta{font-size:12px;color:var(--sub);margin:3px 0 6px;}
.tag{display:inline-block;padding:1px 7px;border-radius:6px;font-size:11px;font-weight:600;margin-right:3px;}
.tag.dir{background:#E7F1ED;color:var(--teal);}
.tag.ddl{background:#FBEAE3;color:#B5572A;}
.tag.t1{background:#E4ECF4;color:var(--steel);}
.tag.t2{background:#E7F1ED;color:var(--teal);}
.tag.t3{background:#FBEFD9;color:#9A6A12;}
.resp{display:inline-block;padding:1px 8px;border-radius:6px;font-size:11.5px;font-weight:700;background:#EEF2F7;color:#46525E;}
.ddlchip{display:inline-block;padding:1px 7px;border-radius:6px;font-size:11px;font-weight:700;background:#FBEAE3;color:#B5572A;margin:2px 3px 0 0;}
.prog{font-size:12.5px;color:var(--ink);margin-top:5px;background:#F7FAFD;border-left:2px solid var(--teal);padding:6px 9px;border-radius:0 6px 6px 0;}
.todos{margin-top:6px;font-size:12.5px;color:#46525E;}
.todos li{margin:2px 0;}
.cn{margin-top:8px;background:#EEF4FB;border-left:3px solid var(--steel);border-radius:0 8px 8px 0;padding:8px 11px;}
.cn-h{font-size:11.5px;font-weight:800;color:var(--steel);margin-bottom:3px;letter-spacing:.3px;}
.cn-part{background:#F7FAFD;border:1px solid #E2EAF3;border-radius:6px;padding:6px 9px;margin:6px 0 8px;font-size:11.5px;line-height:1.55;}
.cn-part-row{display:flex;gap:6px;margin-bottom:3px;align-items:flex-start;}
.cn-part-row:last-child{margin-bottom:0;}
.cn-label{flex-shrink:0;display:inline-block;padding:1px 7px;border-radius:5px;font-size:10.5px;font-weight:700;background:#E4ECF4;color:var(--steel);min-width:42px;text-align:center;line-height:1.4;}
.cn-label.self{background:#E7F1ED;color:var(--teal);}
.cn-n{flex:1;color:var(--ink);}
.cn-n .em{color:var(--sub);font-size:10.5px;margin-left:4px;}
.cn-sec{margin-top:7px;font-size:12px;color:var(--ink);line-height:1.55;}
.cn-sec-title{font-size:11.5px;font-weight:800;letter-spacing:.3px;margin-bottom:2px;}
.cn-sec-items{margin:2px 0 0 0;padding:0;list-style:none;counter-reset:cnli;}
.cn-sec-items li{position:relative;padding:2px 0 2px 22px;counter-increment:cnli;}
.cn-sec-items li::before{content:counter(cnli);position:absolute;left:4px;top:2px;display:inline-block;width:14px;height:14px;line-height:14px;text-align:center;border-radius:50%;background:#D9E2EC;color:#46525E;font-size:10px;font-weight:800;}
.cn-sec.ia .cn-sec-title{color:#B5572A;}
.cn-sec.ia .cn-sec-items li::before{background:#F6D6D2;color:#9C3B33;}
.cn-sec.notes .cn-sec-title{color:var(--teal);}
.cn-sec.notes .cn-sec-items li::before{background:#E7F1ED;color:var(--teal);}
.risk{margin-top:7px;font-size:12px;font-weight:600;color:#B5572A;background:#FBF1E9;border-radius:6px;padding:4px 8px;}
.cn-empty{margin-top:6px;font-size:11.5px;color:#9AA0A6;}
.mc-block,.todo-block{margin-top:8px;}
.mc-body{font-size:12.5px;color:#46525E;}
.ia{color:#9A6A12;font-weight:600;}
.todo-actions{display:flex;gap:6px;margin-top:8px;flex-wrap:wrap;}
/* 中英文对照双语行（用户最新规则）：主要内容 / 待办事项 */
.bi-row{display:flex;flex-direction:column;gap:2px;margin:3px 0;}
.bi-cn{font-size:12.5px;color:var(--ink);line-height:1.55;font-weight:500;}
.bi-cn b.cn-no{color:var(--steel);margin-right:3px;}
.bi-en{font-size:11.2px;color:var(--sub);padding:2px 0 2px 10px;border-left:2px solid #DAE3EC;line-height:1.5;font-style:italic;}
.bi-en::before{content:"🔤 EN";color:#5E7DA0;font-style:normal;font-weight:700;margin-right:5px;font-size:10.5px;letter-spacing:.3px;}
.bi-empty{font-size:11.5px;color:#9AA0A6;font-style:italic;}
.todos li{list-style:none;margin:0;padding:6px 0;border-bottom:1px dashed #EFF2F6;}
.todos li:last-child{border-bottom:none;}
.ta-btn{cursor:pointer;font-size:11.5px;padding:2px 11px;border-radius:99px;border:1px solid var(--line);background:#fff;color:var(--sub);user-select:none;transition:.12s;display:inline-flex;align-items:center;gap:4px;}
.ta-btn:hover{filter:brightness(0.96);}
/* 常态即三色 —— 已回复 绿 / 待回复 琥珀 / 无需回复 灰 */
.ta-btn[data-st="replied"]{background:#E6F4EA;color:#1E7A3C;border-color:#B7DFC4;}
.ta-btn[data-st="pending"]{background:#FBEFD9;color:#9A6A12;border-color:#E3C98C;}
.ta-btn[data-st="none"]{background:#EFEEF0;color:#5C6470;border-color:#D8D9DD;}
/* 选中态加深 + 阴影 */
.ta-btn.on[data-st="replied"]{background:#1E7A3C;color:#fff;border-color:#1E7A3C;box-shadow:0 1px 0 rgba(30,122,60,.25);}
.ta-btn.on[data-st="pending"]{background:#B5791F;color:#fff;border-color:#B5791F;box-shadow:0 1px 0 rgba(181,121,31,.25);}
.ta-btn.on[data-st="none"]{background:#5C6470;color:#fff;border-color:#5C6470;box-shadow:0 1px 0 rgba(92,100,112,.25);}
.done-bar{font-size:12px;color:var(--sub);padding:4px 0 8px;}
.done-reset{cursor:pointer;color:var(--steel);font-weight:600;}
.done-reset:hover{text-decoration:underline;}
.thread.done{opacity:.72;padding:6px 12px;border:1px dashed var(--line);border-radius:8px;background:#FAFAFB;font-size:12.5px;color:var(--sub);margin-bottom:8px;}
.done-mark{color:#1E7A3C;font-weight:700;margin-right:6px;}
.done-restore{cursor:pointer;color:var(--steel);margin-left:6px;font-weight:600;}
.done-restore:hover{text-decoration:underline;}
tr.done{opacity:.6;}
tr.done td{text-decoration:line-through;color:#9AA0A6;}
/* 需反馈且有截止：浅红突出 + 置顶 */
.urgent{background:#FCEBE9 !important;border-left:3px solid #D98A8A;}
.urgent:hover{background:#F9DEDB !important;}
.urgent .tag.ddl{background:#F6D6D2;color:#9C3B33;}
.fb-badge{display:inline-block;padding:1px 7px;border-radius:6px;font-size:11px;font-weight:700;background:#D98A8A;color:#fff;margin-left:5px;vertical-align:middle;}
.chase-banner{background:#FCEBE9;border:1px solid #EBC4C0;border-radius:10px;padding:9px 13px;margin-bottom:12px;font-size:13px;color:#9C3B33;font-weight:600;}
.chase-banner b{color:#7A2E28;}
.chase-banner.ok{background:#EEF6F2;border-color:#CDE3D8;color:#3E8E80;}
table{width:100%;border-collapse:collapse;font-size:13px;}
th,td{text-align:left;padding:9px 9px;border-bottom:1px solid var(--line);vertical-align:top;}
th{background:#F2F5F9;color:var(--sub);font-weight:600;font-size:12px;position:sticky;top:0;}
tbody tr:hover{background:#F7FAFD;}
.tbl-scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;margin-bottom:10px;border:1px solid var(--line);border-radius:10px;background:#fff;}
.tbl-scroll table{min-width:640px;}
.content{color:var(--ink);max-width:520px;}
.src{color:var(--sub);font-size:12px;}
.note{margin-top:16px;font-size:12px;color:var(--sub);border-top:1px dashed var(--line);padding-top:11px;}
.empty{color:var(--sub);padding:22px;text-align:center;}

/* 临期事项待办提醒 */
.reminder{background:linear-gradient(135deg,#FFF8EE,#FDEFE2);border:1px solid #EAD3B0;border-radius:12px;padding:12px 15px;margin-bottom:16px;}
.rem-head{font-size:13.5px;font-weight:700;color:var(--ochre);margin-bottom:8px;}
.rem-head b{font-size:16px;}
.rem-groups{display:flex;flex-direction:column;gap:8px;margin-top:6px;}
.rem-section{border:1px solid var(--line);border-radius:8px;background:#fff;overflow:hidden;}
.rem-section-head{background:#F7F4EC;padding:5px 12px;font-weight:700;font-size:12.5px;border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;}
.rem-section-head .cnt{background:#fff;border:1px solid var(--line);padding:1px 8px;border-radius:99px;font-size:11px;color:var(--sub);}
.rem-row{display:flex;gap:10px;align-items:center;padding:6px 12px;cursor:pointer;border-bottom:1px solid var(--line);font-size:12.5px;}
.rem-row:last-child{border-bottom:none;}
.rem-row:hover{background:#FAFCFE;}
.rem-date{flex-shrink:0;color:var(--sub);font-weight:600;font-size:12px;width:84px;}
.rem-proj{flex-shrink:0;width:144px;font-size:12.5px;color:var(--ink);}
.rem-proj b{color:var(--steel);font-weight:700;}
.rem-action{font-size:10.5px;color:#9A6A12;background:#FBEFD9;border:1px solid #E3C98C;padding:1px 7px;border-radius:99px;margin-left:5px;font-weight:600;}
.rem-detail{flex:1;color:#46525E;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.rem-go{flex-shrink:0;color:var(--steel);font-weight:700;font-size:11.5px;cursor:pointer;}
.rem-actions{display:flex;align-items:center;gap:6px;flex-shrink:0;margin-left:auto;}
.rem-done-btn{flex-shrink:0;font-size:11px;color:#1E7A3C;background:#E6F4EA;border:1px solid #B7DFC4;padding:2px 9px;border-radius:99px;cursor:pointer;font-weight:600;white-space:nowrap;user-select:none;transition:.12s;}
.rem-done-btn:hover{background:#1E7A3C;color:#fff;}
.rem-done-btn:active{transform:scale(.96);}

/* Monica 高亮（西葡模块） */
.monica-badge{display:inline-block;padding:1px 8px;border-radius:6px;font-size:11px;font-weight:800;background:#F3E6C8;color:#8A6A1E;margin-left:5px;vertical-align:middle;}
.monica-hl{border-left:3px solid var(--ochre);background:#FFFBF2;}
.country-tag{display:inline-block;padding:1px 7px;border-radius:6px;font-size:11px;font-weight:700;background:#EAF0E6;color:#4E7A3E;margin-right:3px;}

/* ===== 手机 / 窄屏适配（飞书附件手机打开即浏览器渲染） ===== */
@media(max-width:820px){
  body{font-size:15px;}
  .wrap{padding:14px 12px 40px;}
  header.top{padding:14px 16px;}
  header.top h1{font-size:18px;}
  .topbar .tabs{margin:10px 0 0;}
  .tabs{overflow-x:auto;flex-wrap:nowrap;-webkit-overflow-scrolling:touch;padding-bottom:4px;}
  .tab{padding:8px 14px;font-size:13px;flex-shrink:0;}
  .panel{padding:12px 12px;}
  .kpis{gap:8px;}
  .kpi{min-width:calc(50% - 4px);flex:1 1 calc(50% - 4px);padding:10px 12px;}
  .kpi .n{font-size:21px;}
  .charts{flex-direction:column;}
  .chart{min-width:0;}
  .bars{height:120px;}
  .content{max-width:100%;}
  .thread{padding:10px 12px;}
  .thread .th{font-size:14px;}
  .storebtns{overflow-x:auto;flex-wrap:nowrap;-webkit-overflow-scrolling:touch;padding-bottom:4px;}
  .sbtn{flex-shrink:0;}
  .toolbar{flex-direction:column;align-items:stretch;}
  .toolbar input,.toolbar select{width:100%;min-width:0;}
  .bi-cn{font-size:13px;}
  .bi-en{font-size:11.5px;}
  .rem-head{font-size:12.5px;}
  .rem-head b{font-size:15px;}
  .rem-row{flex-wrap:wrap;gap:4px 8px;padding:8px 10px;}
  .rem-date{width:auto;}
  .rem-proj{width:auto;}
  .rem-detail{white-space:normal;flex-basis:100%;order:3;}
  .rem-go{margin-left:auto;}
  table,th,td{font-size:13px;}
  th,td{padding:8px 8px;}
}
@media(max-width:480px){
  .kpis{gap:6px;}
  .kpi{flex-basis:100%;min-width:0;}
  header.top h1{font-size:16px;}
  header.top .meta{font-size:11px;}
  .subhead{font-size:14px;}
}
</style>
</head>
<body>
<div class="wrap">
<div class="topbar">
<header class="top">
  <h1>飞书邮件工作看板 · 往来 Summary / 西南欧建店 / 西葡非建店 / 其他事项</h1>
  <div class="meta">邮箱 __ME__ ｜ 数据窗口 __WIN__ ｜ 生成时间 __GEN__ ｜ 来源：WorkBuddy 飞书连接器本地生成</div>
</header>

<div class="tabs">
  <div class="tab active" data-t="vol">① 往来邮件 Summary</div>
  <div class="tab" data-t="store">② 西南欧建店管理</div>
  <div class="tab" data-t="iberia">③ 西葡地区非建店业务跟踪</div>
  <div class="tab" data-t="todo">④ 其他事项（下单/交付/交期）</div>
</div>
</div>

<!-- TAB 1: volume + 临期提醒 -->
<div class="panel active" id="p_vol">
  <div class="reminder" id="reminder"></div>
  <div class="kpis" id="kpis"></div>
  <div class="charts">
    <div class="chart"><h3>邮件按月份分布（往来总量）</h3><div class="bars" id="bar_month"></div></div>
    <div class="chart"><h3>按关键门店分布</h3><div class="bars" id="bar_store"></div></div>
    <div class="chart"><h3>收 / 发 方向</h3><div class="bars" id="bar_dir"></div></div>
  </div>
  <div class="note">说明：往来数量仅作背景参考。窗口内共 <b>__TOTAL__</b> 封邮件，其中收到 __REC__ / 发出 __SENT__；旗标 __FLAG__ 封；含明确 DDL __DDL__ 条；涉及 4 个重点门店 __KEY__ 封；西葡非建店业务 __IB__ 个线程（Monica 涉及 __IBM__ 个）。图表为自包含渲染（无外部依赖）。</div>
</div>

<!-- TAB 2: store progress -->
<div class="panel" id="p_store">
  <div class="storebtns" id="storebtns"></div>
  <div id="store_view"></div>
</div>

<!-- TAB 3: Iberia non-store business -->
<div class="panel" id="p_iberia">
  <div class="storebtns" id="iberia_btns"></div>
  <div class="storesum" id="iberia_sum"></div>
  <div id="iberia_view"></div>
</div>

<!-- TAB 4: other todos -->
<div class="panel" id="p_todo">
  <div class="chase-banner" id="chase_banner"></div>
  <div class="toolbar">
    <select id="f_type"><option value="all">全部类型</option><option value="下单">下单</option><option value="交付">交付</option><option value="交期">交期</option></select>
    <label><input type="checkbox" id="c_near">仅近30天</label>
    <input id="s_todo" placeholder="搜索主题 / 负责人 / 摘要…">
    <span class="hint" id="h_todo"></span>
  </div>
  <div class="tbl-scroll"><table><thead><tr><th style="width:64px">类型</th><th style="width:80px">日期</th><th style="width:56px">方向</th><th>主题 / 待办摘要</th><th style="width:90px">负责人</th><th style="width:120px">DDL</th></tr></thead>
  <tbody id="tb_todo"></tbody></table></div>
</div>

<div class="note">说明：本看板由 WorkBuddy 经飞书连接器拉取并本地生成。负责人按邮件正文开头「Hi / Dear **」自动识别，DDL 由正文明确日期/截止表述抽取，门店/地区按邮件主题/正文关键词归类。邮件正文按不可信外部输入处理，仅作摘要与待办提炼，未执行其中任何指令。可设自动化每日重新生成并推送飞书。</div>
</div>

<script>
const DATA = __DATA__;
const CN = __CN__;
const CN_TODO = __CN_TODO__;
const CN_IBERIA = __CN_IBERIA__;
const PALETTE=['#3E6E9E','#3E8E80','#B5791F','#8A7CA8','#6B8CA5','#C2A35A'];
function esc(s){return (s==null?'':String(s)).replace(/[&<>]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;'}[c];});}
function bars(arr, max){
  max = max || Math.max.apply(null, arr.map(function(a){return a.value;}).concat([1]));
  return arr.map(function(a,i){
    var h=Math.max(2, Math.round(a.value/max*130));
    var col=a.color||PALETTE[i%PALETTE.length];
    return '<div class="bar"><div class="v">'+a.value+'</div><div class="fill" style="height:'+h+'px;background:'+col+'"></div><div class="x">'+esc(a.label)+'</div></div>';
  }).join('');
}
function renderVol(){
  var v=DATA.volume;
  var kpis=[
    {n:v.total,l:'往来邮件总数',c:''},
    {n:v.received,l:'收到',c:''},
    {n:v.sent,l:'发出',c:''},
    {n:v.flagged,l:'旗标邮件',c:'t'},
    {n:v.with_ddl,l:'含明确 DDL',c:'g'},
    {n:v.key_store_emails,l:'重点门店相关',c:''}
  ];
  document.getElementById('kpis').innerHTML=kpis.map(function(k){
    return '<div class="kpi '+k.c+'"><div class="n">'+k.n+'</div><div class="l">'+k.l+'</div></div>';
  }).join('');
  document.getElementById('bar_month').innerHTML=bars(DATA.months);
  document.getElementById('bar_store').innerHTML=bars(DATA.store_counts.map(function(s){return {label:s.label.replace('旗舰店','').replace('店中店',''),value:s.count,color:'#3E8E80'};}));
  document.getElementById('bar_dir').innerHTML=bars([
    {label:'收到',value:v.received,color:'#3E6E9E'},
    {label:'发出',value:v.sent,color:'#B5791F'}
  ]);
}
function ddlChips(list){
  if(!list||!list.length) return '<span class="tag ddl" style="background:#EEF1F4;color:#9AA0A6">—</span>';
  return list.slice(0,3).map(function(d){return '<span class="ddlchip">'+esc(d.date)+'</span>';}).join('');
}
function partyCell(arr){
  if(!arr||!arr.length) return '<span class="cn-n" style="color:#9AA0A6">—</span>';
  return arr.map(function(p){
    if(!p) return '';
    var n=esc(p.name||''); var em=esc(p.email||'');
    if(!n && !em) return '';
    return (n||em)+(p.email && p.name?' <span class="em">&lt;'+em+'&gt;</span>':'');
  }).filter(Boolean).join(' · ')|| '<span class="cn-n" style="color:#9AA0A6">—</span>';
}
// 参与方：仅显示 发件人 + 收件人；抄送(CC) 一律不显示（含姓名与邮箱）
function partiesBlock(p){
  if(!p) return '';
  var fr=p.from?('<div class="cn-part-row"><span class="cn-label">发件人</span><span class="cn-n">'+partyCell([p.from])+'</span></div>'):'';
  var to=p.to&&p.to.length?('<div class="cn-part-row"><span class="cn-label">收件人</span><span class="cn-n">'+partyCell(p.to)+'</span></div>'):'';
  return fr+to?'<div class="cn-part">'+fr+to+'</div>':'';
}
function sectionList(title, items, klass){
  if(!items||!items.length) return '';
  return '<div class="cn-sec '+(klass||'')+'"><div class="cn-sec-title">'+title+'</div>'+
    '<ol class="cn-sec-items">'+items.map(function(x){return '<li>'+esc(x)+'</li>';}).join('')+'</ol></div>';
}
/* --- CN 兜底链（支持 summary/todos 与 items/needs_action 两种词典风格） --- */
function cnSummary(cn){
  if(!cn) return '';
  if(cn.summary) return cn.summary;
  if(cn.needs_action && cn.needs_action.length) return cn.needs_action.join('；');
  if(cn.items && cn.items.length) return cn.items.join('；');
  return '';
}
function cnTodosArr(cn){
  if(!cn) return [];
  if(cn.todos && cn.todos.length) return cn.todos.slice(0);
  var arr=[];
  if(cn.needs_action && cn.needs_action.length) arr.push.apply(arr, cn.needs_action);
  if(cn.items && cn.items.length) arr.push.apply(arr, cn.items);
  if(cn.party_notes && cn.party_notes.length) arr.push.apply(arr, cn.party_notes);
  return arr;
}
/* 中英文对照块：单行中文 + 缩进英文小字（用于主要内容）
   用户最新规则：CN 词典缺失时，用 trSubj 对英文做兜底中文翻译 */
function mainContentBlock(cnObj, progressEn){
  var cnText = cnSummary(cnObj);
  var enRaw = (progressEn || '').trim();
  /* 兜底翻译：若 CN 词典缺失，对英文原文做模式字典翻译 */
  if(!cnText && enRaw) cnText = trSubj(enRaw);
  if(!cnText && !enRaw) return '<div class="bi-row"><div class="bi-empty">（暂无主要内容）</div></div>';
  var html = '<div class="bi-row">';
  if(cnText) html += '<div class="bi-cn">'+esc(cnText)+'</div>';
  if(enRaw){
    var enCut = enRaw.length>280 ? enRaw.slice(0,280)+'…' : enRaw;
    html += '<div class="bi-en">'+esc(enCut)+'</div>';
  }
  html += '</div>';
  return html;
}
/* 中英文对照块：每个待办项目一对（中上 + EN 缩进下）
   用户最新规则：CN 词典缺失时，用 trSubj 对英文做兜底中文翻译 */
function todoBilingualList(cnObj, enArr){
  var cnArr = cnTodosArr(cnObj);
  var en = enArr || [];
  var hasCn = cnArr.length > 0;
  /* 如果 CN 词典没有现成摘要，但有英文原待办，逐项做兜底翻译 */
  if(!hasCn && en.length){
    cnArr = en.map(function(x){ return trSubj(x||'') || ''; });
    hasCn = cnArr.some(function(x){ return x && /[\u4e00-\u9fa5]/.test(x); });
  }
  var max = Math.max(cnArr.length, en.length);
  if(max===0) return '<div class="bi-row"><div class="bi-empty">（无明确待办语句）</div></div>';
  var rows=[];
  for(var i=0; i<max; i++){
    var cnLine = cnArr[i] || '';
    var enLine = en[i] || '';
    var no = i+1;
    var row = '<li>';
    if(hasCn){
      row += '<div class="bi-cn"><b class="cn-no">'+no+'.</b>'+esc(cnLine || '—')+'</div>';
      if(enLine) row += '<div class="bi-en">'+esc(enLine)+'</div>';
    }else{
      /* 兜底都未命中：仅显示原文 */
      row += '<div class="bi-en" style="font-style:normal;border-left-color:#DAE3EC"><b class="cn-no" style="color:var(--steel);font-style:normal;margin-right:4px">'+no+'.</b>'+esc(enLine)+'</div>';
    }
    row += '</li>';
    rows.push(row);
  }
  return '<ol class="todos">'+rows.join('')+'</ol>';
}
function cnBlock(t, key){
  var cn=(CN[key]||{})[t.thread_id];
  if(!cn) return '';
  var parts=partiesBlock(cn.participants);
  /* 主块展示中文 summary（用户最新词典键名）；副块保留 needs_action / party_notes */
  var secSum=cn.summary?('<div class="cn-sec"><div class="cn-sec-title">中文摘要</div><div class="bi-cn" style="margin:2px 0 4px">'+esc(cn.summary)+'</div></div>'):'';
  var secIA=cn.needs_action&&cn.needs_action.length?sectionList('需你确认或反馈', cn.needs_action, 'ia'):'';
  var secN=cn.party_notes&&cn.party_notes.length?sectionList('对方告知事项（含发件人休假等）', cn.party_notes, 'notes'):'';
  var risk=cn.risk?('<div class="risk">⚠ 风险：'+esc(cn.risk)+'</div>'):'';
  return '<div class="cn"><div class="cn-h">🇨🇳 邮件摘要翻译</div>'+
    parts+ secSum+ secIA+ secN+ risk+'</div>';
}
function cnTodoBlock(cn){
  if(!cn) return '';
  var parts=partiesBlock(cn.participants);
  var secSum=cn.summary?('<div class="cn-sec"><div class="cn-sec-title">中文摘要</div><div class="bi-cn" style="margin:2px 0 4px">'+esc(cn.summary)+'</div></div>'):'';
  var secIA=cn.needs_action&&cn.needs_action.length?sectionList('需你确认或反馈', cn.needs_action, 'ia'):'';
  var secN=cn.party_notes&&cn.party_notes.length?sectionList('对方告知事项（含发件人休假等）', cn.party_notes, 'notes'):'';
  var risk=cn.risk?('<div class="risk">⚠ 风险：'+esc(cn.risk)+'</div>'):'';
  return '<div class="cn"><div class="cn-h">🇨🇳 邮件摘要翻译</div>'+
    parts+ secSum+ secIA+ secN+ risk+'</div>';
}
function threadCard(t, key){
  var tid='st_'+t.thread_id;
  if(isDismissed(tid)) return '<div class="thread done" id="'+tid+'"><span class="done-mark">✓ 已处理</span> '+esc(t.subject)+' <span class="done-restore" onclick="markTodo(\''+tid+'\',\'\')">↺ 恢复</span></div>';
  var resp=t.responsible?('<span class="resp">'+esc(t.responsible)+'</span>'):'';
  var dirs=t.dirs.map(function(x){return '<span class="tag dir">'+esc(x)+'</span>';}).join(' ');
  var cn=(CN[key]||{})[t.thread_id];
  var cnTag=cn?'<span class="tag t1">已译</span>':'';
  /* 主要内容：中英文对照（用户最新规则） */
  var mainC=mainContentBlock(cn, t.progress);
  /* 待办事项：中英文对照（每条 中文行 + EN 缩进行） */
  var todoC='<div class="todo-block"><div class="cn-h">✅ 待办事项</div>'+todoBilingualList(cn, t.todos)+'</div>';
  return '<div class="thread" id="'+tid+'"><div class="th">'+esc(t.subject)+'</div>'+
    '<div class="meta">'+esc(t.first)+' → '+esc(t.last)+' ｜ '+t.count+' 封 ｜ '+dirs+' ｜ '+resp+' ｜ '+cnTag+'</div>'+
    '<div>'+ddlChips(t.ddl)+'</div>'+
    (cn?(cnBlock(t,key)):'<div class="cn-empty">（本线程暂未纳入翻译范围；可在下个自动化周期补充）</div>')+
    '<div class="mc-block"><div class="cn-h">📌 主要内容</div>'+mainC+'</div>'+
    todoC+
    todoActionBarHTML(tid)+'</div>';
}
function renderStore(key){
  curStoreKey=key;
  var sv=DATA.stores[key];
  var tids=[]; sv.sections.forEach(function(s){ s.items.forEach(function(it){ tids.push('st_'+it.thread_id); }); });
  var html='<div class="storesum">邮件 '+sv.emails+' 封';
  sv.sections.forEach(function(s){ html+=' ｜ '+esc(s.sub)+'：'+s.count+' 封 / '+s.threads+' 线程 / 含DDL '+s.with_ddl; });
  html+='</div>'+doneBarHTML(tids);
  sv.sections.forEach(function(s){
    html+='<div class="subhead">'+esc(s.sub)+'（'+s.count+' 封 / '+s.threads+' 线程）</div>';
    html+=s.items.map(function(it){return threadCard(it, key);}).join('');
  });
  document.getElementById('store_view').innerHTML=html;
}
function bindStoreBtns(){
  var keys=['Cologne','Rome','Dusseldorf','Zurich'];
  var box=document.getElementById('storebtns');
  box.innerHTML=keys.map(function(k){
    var sv=DATA.stores[k];
    return '<div class="sbtn" data-k="'+k+'">'+esc(sv.label)+'<span class="c">'+sv.emails+'</span></div>';
  }).join('');
  box.querySelectorAll('.sbtn').forEach(function(b){
    b.addEventListener('click',function(){
      box.querySelectorAll('.sbtn').forEach(function(x){x.classList.remove('active');});
      b.classList.add('active');
      renderStore(b.getAttribute('data-k'));
    });
  });
  box.querySelector('.sbtn').classList.add('active');
  renderStore('Cologne');
}
/* ---------- 西葡地区非建店业务 ---------- */
function iberiaCard(t){
  var tid='ib_'+t.thread_id;
  if(isDismissed(tid)) return '<div class="thread done" id="'+tid+'"><span class="done-mark">✓ 已处理</span> '+esc(t.subject)+' <span class="done-restore" onclick="markTodo(\''+tid+'\',\'\')">↺ 恢复</span></div>';
  var dirs=t.dirs.map(function(x){return '<span class="tag dir">'+esc(x)+'</span>';}).join(' ');
  var monica=t.monica?'<span class="monica-badge">★ Monica</span>':'';
  var country=t.country?'<span class="country-tag">'+esc(t.country)+'</span>':'';
  var cn=CN_IBERIA[t.thread_id];
  var cnTag=cn?'<span class="tag t1">已译</span>':'';
  var mainC=mainContentBlock(cn, t.progress);
  var todoC='<div class="todo-block"><div class="cn-h">✅ 待办事项</div>'+todoBilingualList(cn, t.todos)+'</div>';
  return '<div class="thread'+(t.monica?' monica-hl':'')+'" id="'+tid+'"><div class="th">'+esc(t.subject)+'</div>'+
    '<div class="meta">'+esc(t.first)+' → '+esc(t.last)+' ｜ '+t.count+' 封 ｜ '+dirs+' ｜ '+country+' ｜ '+monica+' ｜ '+cnTag+'</div>'+
    '<div>'+ddlChips(t.ddl)+'</div>'+
    (cn?(cnBlock(t,'iberia')):'<div class="cn-empty">（本线程暂未纳入翻译范围；可在下个自动化周期补充）</div>')+
    '<div class="mc-block"><div class="cn-h">📌 主要内容</div>'+mainC+'</div>'+
    todoC+
    todoActionBarHTML(tid)+'</div>';
}
function renderIberia(type){
  curIberiaType=type;
  var secs=DATA.iberia_view.sections.filter(function(s){return type==='all'||s.type===type;});
  var tids=[]; secs.forEach(function(s){ s.items.forEach(function(it){ tids.push('ib_'+it.thread_id); }); });
  var html=''; var total=0;
  secs.forEach(function(s){
    total+=s.count;
    html+='<div class="subhead">'+esc(s.type)+'（'+s.count+' 线程）</div>';
    html+=s.items.map(function(t){return iberiaCard(t);}).join('');
  });
  document.getElementById('iberia_sum').innerHTML='西葡非建店业务：共 '+total+' 个线程，Monica 涉及 '+DATA.iberia_view.monica_count+' 个（★ 高亮为 Monica 参与的邮件）';
  var out=(total?doneBarHTML(tids):'')+html;
  document.getElementById('iberia_view').innerHTML=out||'<div class="empty">无匹配</div>';
}
function bindIberiaBtns(){
  var types=['all'].concat(DATA.iberia_view.sections.map(function(s){return s.type;}));
  var box=document.getElementById('iberia_btns');
  box.innerHTML=types.map(function(tp){
    var label=tp==='all'?'全部':tp;
    var cnt = tp==='all'?DATA.iberia_view.total:(DATA.iberia_view.sections.filter(function(s){return s.type===tp;})[0]||{count:0}).count;
    return '<div class="sbtn" data-tp="'+tp+'">'+label+'<span class="c">'+cnt+'</span></div>';
  }).join('');
  box.querySelectorAll('.sbtn').forEach(function(b){
    b.addEventListener('click',function(){
      box.querySelectorAll('.sbtn').forEach(function(x){x.classList.remove('active');});
      b.classList.add('active');
      renderIberia(b.getAttribute('data-tp'));
    });
  });
  box.querySelector('.sbtn').classList.add('active');
  renderIberia('all');
}
/* ---------- 其他事项 ---------- */
function renderTodo(){
  var ty=document.getElementById('f_type').value;
  var near=document.getElementById('c_near').checked;
  var q=document.getElementById('s_todo').value.toLowerCase();
  /* 用户最新规则：抓取/统计窗口收紧到 7 天；near 过滤也用 7 天界 */
  var nearCut = DATA.near30_cut; /* 已与 -30 天对应；下面再覆盖为近 7 天 */
  var nd = new Date(DATA.today+'T00:00:00');
  var near7 = new Date(nd.getTime() - 7*86400000);
  nearCut = near7.toISOString().slice(0,10);
  var rows=DATA.other_todos.filter(function(it){
    if(ty!=='all' && it.type!==ty) return false;
    if(near && it.date && it.date < nearCut) return false;
    if(q){ var hay=(it.subject+' '+(it.responsible||'')+' '+it.summary+' '+(it.todos||[]).join(' ')).toLowerCase(); if(hay.indexOf(q)<0) return false; }
    return true;
  });
  rows.sort(function(a,b){
    var ua=(a.needs_feedback?1:0), ub=(b.needs_feedback?1:0);
    if(ua!==ub) return ub-ua;
    var da=a.ddl_earliest||'9999', db=b.ddl_earliest||'9999';
    if(da!==db) return da<db?-1:1;
    return 0;
  });
  var cls={'下单':'t1','交付':'t2','交期':'t3'};
  var urgentTotal=DATA.other_todos.filter(function(x){return x.needs_feedback;}).length;
  document.getElementById('chase_banner').innerHTML = urgentTotal
    ? ('⏰ <b>'+urgentTotal+'</b> 项需反馈且临近截止（看板已用浅红标红并置顶最上方）')
    : '暂无「需反馈且有截止」的待办';
  var tb=document.getElementById('tb_todo');
  tb.innerHTML=rows.length?rows.map(function(it){
    var urg=it.needs_feedback?' urgent':'';
    var tid='ot_'+it.id;
    var doneCls=isDismissed(tid)?' done':'';
    var badge=it.needs_feedback?'<span class="fb-badge">需反馈</span>':'';
    var cnBadge=CN_TODO[it.id]?'<span class="tag t1" style="margin-left:4px">已译</span>':'';
    /* 中英文对照（用户最新规则）：主要内容 + 待办事项 都双语 */
    var cnObj = CN_TODO[it.id] || null;
    var cnSub = cnSummary(cnObj);
    /* 用户最新规则：若 CN 词典缺失，用 trSubj 对英文主题/摘要/待办做兜底翻译（仍展示英文原文） */
    var trSubjFallback = cnSub || trSubj(it.subject||'');
    var mainBi = mainContentBlock(cnObj, it.summary);
    var todoBi = todoBilingualList(cnObj, it.todos);
    var subjHtml = '<div class="src" style="font-weight:600;color:var(--ink);margin-bottom:3px"><b>📌 主题</b> '+esc(it.subject)+cnBadge+'</div>';
    if(trSubjFallback) subjHtml += '<div class="src" style="color:var(--steel);font-weight:600;margin-bottom:5px"><b>📌 主题·中文</b> '+esc(trSubjFallback)+'</div>';
    var act=todoActionBarHTML(tid);
    var cnHtml=CN_TODO[it.id]?'<tr class="todo-cn-row"><td colspan="6" style="background:#FAFCFE;padding:4px 9px 10px;border-bottom:1px solid var(--line)">'+cnTodoBlock(CN_TODO[it.id])+'</td></tr>':'';
    return '<tr class="'+urg.trim()+doneCls+'" id="'+tid+'"><td><span class="tag '+cls[it.type]+'">'+it.type+'</span>'+badge+'</td>'+
      '<td>'+esc(it.date)+'</td>'+
      '<td><span class="tag dir">'+esc(it.direction)+'</span></td>'+
      '<td class="content">'+subjHtml+
        '<div class="mc-block"><div class="cn-h">📌 主要内容</div>'+mainBi+'</div>'+
        '<div class="todo-block"><div class="cn-h">✅ 待办事项</div>'+todoBi+'</div>'+
        act+'</td>'+
      '<td>'+(it.responsible?'<span class="resp">'+esc(it.responsible)+'</span>':'<span class="resp" style="background:#EEF1F4;color:#9AA0A6">未识别</span>')+'</td>'+
      '<td>'+ddlChips(it.ddl)+'</td></tr>'+cnHtml;
  }).join(''):'<tr><td colspan="6" class="empty">无匹配</td></tr>';
  var tids=DATA.other_todos.map(function(x){return 'ot_'+x.id;});
  var doneN=tids.filter(isDismissed).length;
  document.getElementById('h_todo').innerHTML='共 '+rows.length+' 条（下单 '+DATA.stats.other_by_type['下单']+' / 交付 '+DATA.stats.other_by_type['交付']+' / 交期 '+DATA.stats.other_by_type['交期']+'）'+
    (doneN?' ｜ <span class="done-bar">✓ 已处理 '+doneN+' 项 ｜ <span class="done-reset" onclick="resetAllTodos()">↺ 重置</span></span>':'');
}
/* ---------- 临期事项待办提醒 ---------- */
function parseDays(dateStr){
  if(!dateStr) return null;
  var d=new Date(dateStr+'T00:00:00');
  var t=new Date(DATA.today+'T00:00:00');
  if(isNaN(d)||isNaN(t)) return null;
  return Math.round((d-t)/86400000);
}
function urgencyOf(dateStr){
  var days=parseDays(dateStr);
  if(days===null) return null;
  // 提醒窗口收紧为 ±7 天：超过 7 天前的邮件视作已完成/已回复，不在提醒预警范围
  if(days<-7 || days>7) return null;
  // 未来分级（用户最新规则）：距到期 ≤2 天 = 临期；≤5 天 = 关注；>5 天不在提醒窗口
  // 配色：逾期=红 / 临期=黄 / 关注=蓝（用户指定）
  if(days<0) return {lvl:'overdue',label:'已逾期',color:'#C0392B',days:days};
  if(days<=2) return {lvl:'high',label:'临期',color:'#C9A227',days:days};
  if(days<=5) return {lvl:'mid',label:'关注',color:'#2E75B6',days:days};
  return null;
}
function buildReminders(){
  var items=[];
  var seen={};
  function add(src,mod,city,targetId,subject,proj,dd,u){
    var key=targetId+'|'+dd.date;
    if(seen[key]) return; seen[key]=1;
    items.push({
      date:dd.date, src:src, mod:mod, city:city, target:targetId,
      subject:subject||'', proj:proj||'',
      text:((subject||'')+((dd.text)?' — '+dd.text:'')).slice(0,160),
      ddlText:dd.text||'', u:u
    });
  }
  ['Cologne','Rome','Dusseldorf','Zurich'].forEach(function(sk){
    (DATA.stores[sk].sections||[]).forEach(function(sec){
      (sec.items||[]).forEach(function(t){
        if(!(t.todos && t.todos.length)) return; // 无明确待办语句的邮件不计入提醒
        (t.ddl||[]).forEach(function(dd){
          var u=urgencyOf(dd.date);
          if(u) add('西南欧建店','store',sk,'st_'+t.thread_id,t.subject,DATA.stores[sk].label,dd,u);
        });
      });
    });
  });
  (DATA.iberia_view.sections||[]).forEach(function(sec){
    (sec.items||[]).forEach(function(t){
      if(!(t.todos && t.todos.length)) return; // 无明确待办语句的邮件不计入提醒
      (t.ddl||[]).forEach(function(dd){
        var u=urgencyOf(dd.date);
        if(u) add('西葡业务','iberia',null,'ib_'+t.thread_id,t.subject,(t.country||'西葡业务'),dd,u);
      });
    });
  });
  (DATA.other_todos||[]).forEach(function(o){
    (o.ddl||[]).forEach(function(dd){
      var u=urgencyOf(dd.date);
      if(u) add('其他事项','todo',null,'ot_'+o.id,o.subject,(o.type||''),dd,u);
    });
  });
  items.sort(function(a,b){ return a.date<b.date?-1:(a.date>b.date?1:0); });
  return items;
}
/* 邮件主题 → 中文一句话摘要（用于没有 CN 词典时的兜底翻译） */
function trSubj(s){
  if(!s) return '';
  var raw=s;
  /* 0) HTML 实体与编码归一 */
  s=s.replace(/&amp;/gi,'&').replace(/&nbsp;/gi,' ').replace(/&lt;/gi,'<').replace(/&gt;/gi,'>');
  /* 1) 循环剥离链式前缀：R:/RE:/Re:/FW:/AW:/R: … */
  var prev;
  do{ prev=s; s=s.replace(/^\s*(RE|Re|FW|Fw|FYI|AW|Aw|SV|VS|TR|FS|FBL|R)(\s*[：:.\-]\s*)/i,'').trim(); }while(s!==prev && s.length);
  /* 2) 项目级品牌 / 场地 映射 */
  s=s.replace(/\bDE[\s_]+POSM\b/gi,'德国 POSM ');
  s=s.replace(/\bFR[\s_]+POSM\b/gi,'法国 POSM ');
  s=s.replace(/\b11[_\s]*MOVA[_\s]*DE[_\s]*COLOGNE[_\s]*BOUTIQUE[_\s]*MM?[_\s]*/gi,'MOVA 科隆店中店');
  s=s.replace(/\bMOVA[\s_]+DE[\s_]+COLOGNE[\s_]+BOUTIQUE\b/gi,'MOVA 科隆店中店');
  s=s.replace(/\bMOVA[\s_]+Cologne[\s_]+Shop[\s\-‑]*in[\s\-‑]*Shop\b/gi,'MOVA 科隆店中店');
  s=s.replace(/\bGermany[\s_]+D[uü]sseldorf[\s_]+Flagship[\s_]+Store\b/gi,'杜塞旗舰店');
  s=s.replace(/\bDREAME[\s_]+D[uü]sseldorf[\s_]+Flagship[\s_]+Store\b/gi,'DREAME 杜塞旗舰店');
  s=s.replace(/\bD[uü]sseldorf[\s_]+Flagship[\s_]+Store\b/gi,'杜塞旗舰店');
  s=s.replace(/\bTender[\s_]+Invitation\b/gi,'招标邀请');
  s=s.replace(/\bDreame[\s_]+Ital(?:y|ian)[\s_]+MW[\s_]+Robot[\s_]+Vacuum[\s_]+Endcap\b/gi,'DREAME 意大利 MediaWorld 端架');
  s=s.replace(/\bDreame[\s_]+Ital(?:y|ian)[\s_]+Endcap\b/gi,'DREAME 意大利端架');
  s=s.replace(/\bDreame[\s_]+Ital(?:y|ian)[\s_]+POSM\b/gi,'DREAME 意大利 POSM');
  s=s.replace(/\bDreame[\s_]+Ital(?:y|ian)\b/gi,'DREAME 意大利');
  s=s.replace(/\bMOVA[\s_]+Italy[\s_]*[—\-]?\s*Milan\b/gi,'MOVA 意大利米兰');
  s=s.replace(/\bMOVA[\s_]+Italy\b/gi,'MOVA 意大利');
  s=s.replace(/\bDreame[\s_]+0720[\s_]+FR[\s_]+POSM\b/gi,'DREAME 法国 0720 POSM');
  s=s.replace(/\b6\.26[\s_]+POSM[\s_]+Production[\s_]*[—\-]?Italy\b/gi,'6.26 意大利 POSM 生产');
  s=s.replace(/\bPOSM[\s_]+for[\s_]+DE\b/gi,'德国 POSM');
  s=s.replace(/\bAdditional[\s_]+Quotation[\s_]*[—\-]?[\s_]*Electrical[\s_]+Works\b/gi,'增项电气工程报价');
  s=s.replace(/\bPartnership[\s_]+Opportunity[\s_]+for[\s_]+Long[\s_]*[—\-]?Term[\s_]+Printing[\s_]+Collaboration\b/gi,'长期印刷合作');
  s=s.replace(/\bGerman[\s_]+Endcap[\s_]+Request\b/gi,'德国端架申请');
  s=s.replace(/\bStatus[\s_]+check\b/gi,'状态核对');
  s=s.replace(/\bFinal[\s_]+Delivery[\s_]+Date\b/gi,'最终交付日期');
  s=s.replace(/_Status[\s_]+check\b/gi,' 状态核对');
  s=s.replace(/\s+&\s+/g,' · ');
  s=s.replace(/\bPls\s+subject\b.*$/i,'');
  s=s.replace(/^MOVA[\s_]+Italy[\s_]*[—\-]\s*/i,'MOVA 意大利 — ');
  /* 「to Brandart 2026000915」→「 → Brandart」（编号噪声不上板） */
  s=s.replace(/\sto\s+([A-Z][A-Za-z]+)\s+\d{5,}\b/g,' → $1');
  /* 3) 事项动词短语 */
  s=s.replace(/\bRequest\b/g,'申请');
  s=s.replace(/\bevised[\s_]+quotation[\s_]+by[\s_]+(\d{1,2}\w*\s+\w+)/gi,'修订 $1 报价');
  s=s.replace(/\brevised[\s_]+quotation\b/gi,'修订报价');
  s=s.replace(/\bQ&A[\s_]+Period[\s_]+(\d+)[—\-–](\d+)\s*(\w+)?/gi,'答疑期 $1–$2 $3');
  s=s.replace(/\bender[\s_]+Q&A[\s_]+Period\b/gi,'答疑期截止');
  s=s.replace(/\bQ&A[\s_]+Period\b/gi,'答疑期');
  s=s.replace(/\bseparate[\s_]+deliveries\b/gi,'分批交付');
  s=s.replace(/\bschedule[\s_]+(\d+)\s*[—\-–]\s*(\d+)([\s_]+separate)?[\s_]+deliveries\b/gi,'排定 $1–$2 次分批交付');
  s=s.replace(/\bon[\s_]+site[\s_]+on[\s_]+(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)?[\s_]*([\d\.]+)?/gi,'现场到货 $1 $2');
  s=s.replace(/\bam[\s_]+on[\s_]+holiday[\s_]+as[\s_]+of[\s_]+([\d\.]+)[\s_]+until[\s_]+([\d\.]+)/gi,'$1–$2 休假');
  s=s.replace(/\bpreparations?\b/gi,'备货');
  s=s.replace(/\bworking[\s_]+days?\b/gi,'工作日');
  s=s.replace(/\bprint[\s_]+data\b/gi,'印刷数据');
  s=s.replace(/\bshipping[\s_]+time\b/gi,'运输周期');
  s=s.replace(/\bproduction[\s_]+time\b/gi,'生产周期');
  s=s.replace(/\blightboxes?\b/gi,'灯箱');
  s=s.replace(/\bdisplay(?:s)?\b/gi,'陈列道具');
  s=s.replace(/\bendcaps?\b/gi,'端架');
  s=s.replace(/\bRFQ\b/g,'询价');
  s=s.replace(/\bPOSM\b/g,'物料');
  s=s.replace(/\bquotation\b/gi,'报价');
  s=s.replace(/\bnew[\s_]+quotation\b/gi,'新报价');
  s=s.replace(/\bupdated[\s_]+quotation\b/gi,'修订报价');
  s=s.replace(/\btiered[\s_]+pricing\b/gi,'分级报价');
  /* 4) 杂项清理 */
  s=s.replace(/\(\s*We trust that[^)]*\)/gi,'');
  s=s.replace(/\(\s*trust that[^)]*\)/gi,'');
  s=s.replace(/\(We trust\b[^)]*\)/gi,'');
  s=s.replace(/\(we trust\b[^)]*\)/gi,'');
  s=s.replace(/\(to be sent[^)]*\)/gi,'');
  s=s.replace(/\s*[—\-]\s*$/,'').trim();
  s=s.replace(/\s{2,}/g,' ');
  s=s.replace(/\s+([,，。；;])/g,'$1');
  if(!s) s=raw.replace(/^\s*(RE|Re|R|FW|Fw)(\s*[：:.\-]\s*)+/i,'').trim();
  /* 5) 截断 */
  if(s.length>72) s=s.slice(0,72)+'…';
  return s;
}
/* ddl 短语 → 一句话动作（用于主题翻译过短只剩项目名时附加） */
function trAct(t){
  if(!t) return '';
  if(/Q&A Period/i.test(t)) return '答疑期确认';
  if(/schedule[\s_]+\d+/.test(t)) return '排定分批交付计划';
  if(/separate deliveries/i.test(t)) return '确认分批交付';
  if(/on site/i.test(t)) return '现场到货确认';
  if(/holiday/i.test(t)) return '休假通知';
  if(/evised quotation/i.test(t)) return '按期提交报价';
  if(/preparation/i.test(t)) return '备货安排';
  if(/quotation/i.test(t)) return '提交报价';
  if(/Status check|Final Delivery Date/i.test(t)) return '状态核对 / 最终交付日';
  return '';
}
function reminderSummary(i){
  var cn=null, tid=i.target.replace(/^(st_|ib_|ot_)/,'');
  if(i.mod==='store') cn=(CN[i.city]||{})[tid];
  else if(i.mod==='iberia') cn=CN_IBERIA[tid];
  else if(i.mod==='todo') cn=CN_TODO[tid];
  /* 用户最新词典：summary / todos 键优先；旧版 needs_action / items 兜底 */
  var fromCn = cnSummary(cn) || (cnTodosArr(cn)[0] || '');
  var s='';
  if(fromCn) s=fromCn;
  else if(i.subject){
    var tr=trSubj(i.subject);
    /* 若翻译太短（只剩项目名），用 ddl 动作短语补充 */
    if(tr && (tr.length<=10) && i.ddlText){
      var act=trAct(i.ddlText);
      if(act) s=tr+' — '+act;
      else s=tr;
    }else if(tr) s=tr;
    else s=i.subject;
  }else s=i.text||'（无摘要）';
  if(!s||!/[\u4e00-\u9fa5]/.test(s)){
    s='（待人工翻译）'+(i.subject||'').slice(0,30);
  }
  return (s||'（无摘要）').slice(0,90);
}
function renderReminders(){
  var all=buildReminders();
  var items=all.filter(function(i){return !isDismissed(i.target);});
  var dismissedCount=all.length-items.length;
  var box=document.getElementById('reminder');
  if(!items.length && !dismissedCount){
    box.innerHTML='<div class="rem-head" style="color:#3E8E80">📭 当前提醒窗口（逾期7天内 / 未来5天内）暂无临期事项；如有待办临近截止将在此提醒。</div>';
    return;
  }
  if(!items.length){
    box.innerHTML=doneBarRem(dismissedCount)+'<div class="rem-head" style="color:#1E7A3C">✓ 临期提醒已全部处理（'+dismissedCount+' 项已回复/无需回复）。</div>';
    return;
  }
  var groups={
    overdue:{title:'🔴 已逾期',color:'#C0392B',arr:[]},
    high:{title:'🟡 临期（2天内）',color:'#C9A227',arr:[]},
    mid:{title:'🔵 关注（5天内）',color:'#2E75B6',arr:[]}
  };
  items.forEach(function(i){ if(groups[i.u.lvl]) groups[i.u.lvl].arr.push(i); });
  function row(i){
    var proj='<b>'+esc(i.proj||i.src||'')+'</b>';
    var summary=reminderSummary(i);
    var rid=i.target;
    return '<div class="rem-row" title="'+esc(i.subject)+'" onclick="jumpTo(\''+i.mod+'\',\''+i.target+'\''+(i.city?',\''+i.city+'\'':'')+')">'+
      '<span class="rem-date">'+esc(i.date)+'</span>'+
      '<span class="rem-proj">'+proj+'</span>'+
      '<span class="rem-detail">'+esc(summary)+'</span>'+
      '<span class="rem-actions">'+
        '<span class="rem-done-btn" onclick="markTodo(\''+rid+'\',\'replied\');event.stopPropagation();">✓ 已回复</span>'+
        '<span class="rem-go">跳转 →</span>'+
      '</span>'+
    '</div>';
  }
  function section(g){
    if(!g.arr.length) return '';
    return '<div class="rem-section">'+
      '<div class="rem-section-head" style="border-left:3px solid '+g.color+'">'+
        '<span style="color:'+g.color+'">'+g.title+'</span>'+
        '<span class="cnt">'+g.arr.length+' 条</span>'+
      '</div>'+
      g.arr.map(row).join('')+
    '</div>';
  }
  var total=groups.overdue.arr.length+groups.high.arr.length+groups.mid.arr.length;
  /* 标题计数改为 "X 条" 格式（用户最新规则）：已逾期 / 临期 / 关注 具体数量 */
  var head='<div class="rem-head">⏰ 临期事项待办提醒 <b>'+total+'</b> 条 ｜ <span style="color:#C0392B;font-weight:600">已逾期 '+groups.overdue.arr.length+' 条</span> / <span style="color:#C9A227;font-weight:600">临期 '+groups.high.arr.length+' 条</span> / <span style="color:#2E75B6;font-weight:600">关注 '+groups.mid.arr.length+' 条</span> · 点「✓ 已回复」标记已处理（自动消失）或点行跳转邮件</div>';
  var done=doneBarRem(dismissedCount);
  box.innerHTML=done+head+'<div class="rem-groups">'+section(groups.overdue)+section(groups.high)+section(groups.mid)+'</div>';
}
function jumpTo(tab, targetId, city){
  document.querySelectorAll('.tab').forEach(function(x){x.classList.remove('active');});
  document.querySelectorAll('.panel').forEach(function(x){x.classList.remove('active');});
  var tt=document.querySelector('.tab[data-t="'+tab+'"]'); if(tt) tt.classList.add('active');
  var pp=document.getElementById('p_'+tab); if(pp) pp.classList.add('active');
  if(tab==='store' && city){
    var btn=document.querySelector('#storebtns .sbtn[data-k="'+city+'"]');
    if(btn){ document.querySelectorAll('#storebtns .sbtn').forEach(function(x){x.classList.remove('active');}); btn.classList.add('active'); renderStore(city); }
  }
  if(tab==='iberia'){
    var ab=document.querySelector('#iberia_btns .sbtn[data-tp="all"]');
    if(ab){ document.querySelectorAll('#iberia_btns .sbtn').forEach(function(x){x.classList.remove('active');}); ab.classList.add('active'); renderIberia('all'); }
  }
  setTimeout(function(){
    var el=document.getElementById(targetId);
    if(el){ el.scrollIntoView({behavior:'smooth',block:'center'}); el.style.transition='box-shadow .3s'; el.style.boxShadow='0 0 0 3px var(--ochre)'; setTimeout(function(){el.style.boxShadow='';},2200); }
  }, 160);
}
function bindTabs(){
  document.querySelectorAll('.tab').forEach(function(t){
    t.addEventListener('click',function(){
      document.querySelectorAll('.tab').forEach(function(x){x.classList.remove('active');});
      document.querySelectorAll('.panel').forEach(function(x){x.classList.remove('active');});
      t.classList.add('active');
      document.getElementById('p_'+t.getAttribute('data-t')).classList.add('active');
      curTab=t.getAttribute('data-t');
    });
  });
}
/* ---------- 待办状态：已回复/待回复/无需回复（localStorage 持久化） ---------- */
var TODO_STATE={};
var curStoreKey='Cologne', curIberiaType='all', curTab='summary';
function loadTodoState(){ try{TODO_STATE=JSON.parse(localStorage.getItem('wb_todo_state')||'{}');}catch(e){TODO_STATE={};} }
function saveTodoState(){ try{localStorage.setItem('wb_todo_state',JSON.stringify(TODO_STATE));}catch(e){} }
function isDismissed(tid){ var s=TODO_STATE[tid]; return s==='replied'||s==='none'; }
function todoStateOf(tid){ return TODO_STATE[tid]||''; }
function markTodo(tid,st){
  if(TODO_STATE[tid]===st){ delete TODO_STATE[tid]; } else { TODO_STATE[tid]=st; }
  saveTodoState(); rerenderCurrent();
}
function resetAllTodos(){ TODO_STATE={}; saveTodoState(); rerenderCurrent(); }
/* 仅恢复「逾期提醒」中被标记已处理的事项（不影响其他模块的待办状态） */
function resetReminders(){
  buildReminders().forEach(function(i){ delete TODO_STATE[i.target]; });
  saveTodoState(); rerenderCurrent();
}
function doneBarRem(n){
  if(!n) return '';
  return '<div class="done-bar">✓ 已处理 '+n+' 项（已回复/无需回复） ｜ <span class="done-reset" onclick="resetReminders()">↺ 全部恢复</span></div>';
}
function rerenderCurrent(){
  if(curTab==='store') renderStore(curStoreKey);
  else if(curTab==='iberia') renderIberia(curIberiaType);
  else if(curTab==='todo') renderTodo();
  else renderReminders();
}
function todoActionBarHTML(tid){
  var st=todoStateOf(tid);
  var b=function(v,label){ return '<span class="ta-btn'+(st===v?' on':'')+'" data-st="'+v+'" onclick="markTodo(\''+tid+'\',\''+v+'\')">'+label+'</span>'; };
  return '<div class="todo-actions">'+b('replied','已回复')+' '+b('pending','待回复')+' '+b('none','无需回复')+'</div>';
}
function doneBarHTML(tids){
  var n=tids.filter(isDismissed).length;
  if(!n) return '';
  return '<div class="done-bar">✓ 已处理 '+n+' 项 ｜ <span class="done-reset" onclick="resetAllTodos()">↺ 重置</span></div>';
}
function todoBlockFor(t, key, mod){
  var cn=null;
  if(mod==='store') cn=(CN[key]||{})[t.thread_id];
  else if(mod==='iberia') cn=CN_IBERIA[t.thread_id];
  var items=[];
  if(t.todos&&t.todos.length) t.todos.forEach(function(x){ items.push(esc(x)); });
  if(cn&&cn.needs_action&&cn.needs_action.length) cn.needs_action.forEach(function(x){ items.push('<span class="ia">需确认/反馈：</span>'+esc(x)); });
  var body=items.length?('<ul class="todos">'+items.map(function(x){return '<li>'+x+'</li>';}).join('')+'</ul>'):'<div class="todos" style="color:#9AA0A6">（无明确待办语句）</div>';
  return '<div class="todo-block"><div class="cn-h">✅ 待办事项</div>'+body+'</div>';
}
function init(){
  loadTodoState();
  renderVol(); renderReminders(); bindStoreBtns(); bindIberiaBtns(); renderTodo();
  document.getElementById('f_type').addEventListener('change',renderTodo);
  document.getElementById('c_near').addEventListener('change',renderTodo);
  document.getElementById('s_todo').addEventListener('input',renderTodo);
  bindTabs();
  var at=document.querySelector('.tab.active'); if(at) curTab=at.getAttribute('data-t');
}
document.addEventListener('DOMContentLoaded',init);
</script>
</body>
</html>"""

html = (HTML
        .replace('__DATA__', json.dumps(aug, ensure_ascii=False))
        .replace('__CN__', json.dumps(CN_STORES, ensure_ascii=False))
        .replace('__CN_TODO__', json.dumps(CN_TODOS, ensure_ascii=False))
        .replace('__CN_IBERIA__', json.dumps(CN_IBERIA, ensure_ascii=False))
        .replace('__WIN__', aug['window']['start'] + ' ~ ' + aug['window']['end'])
        .replace('__GEN__', aug['generated_at'])
        .replace('__TOTAL__', str(aug['volume']['total']))
        .replace('__REC__', str(aug['volume']['received']))
        .replace('__SENT__', str(aug['volume']['sent']))
        .replace('__FLAG__', str(aug['volume']['flagged']))
        .replace('__DDL__', str(aug['volume']['with_ddl']))
        .replace('__KEY__', str(aug['volume']['key_store_emails']))
        .replace('__IB__', str(aug['stats'].get('iberia', 0)))
        .replace('__IBM__', str(aug['stats'].get('iberia_monica', 0)))
        .replace('__ME__', ME))

with open('mail_workboard2.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('written mail_workboard2.html', len(html), 'bytes; months', len(aug['months']), 'stores', len(aug['store_counts']), 'iberia', aug['stats'].get('iberia',0), 'other_todos', len(aug['other_todos']))
