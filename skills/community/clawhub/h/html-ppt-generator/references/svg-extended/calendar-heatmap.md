# calendar-heatmap · 日历热力图

**适用：** 时间分布（全年/季度/月）、活动频率、提交记录、销售日历
**尺寸：** 160×100px（全年视图）

```html
<svg viewBox="0 0 160 100" style="width:160px;height:100px;flex-shrink:0;" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- 热力色阶（从低到高） -->
    <linearGradient id="chg1" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#1e293b"/>
      <stop offset="100%" stop-color="#334155"/>
    </linearGradient>
  </defs>

  <!-- 月份标签行 -->
  <text x="2" y="8" font-size="7" fill="var(--dt)">Jan</text>
  <text x="16" y="8" font-size="7" fill="var(--dt)">Feb</text>
  <text x="30" y="8" font-size="7" fill="var(--dt)">Mar</text>
  <text x="44" y="8" font-size="7" fill="var(--dt)">Apr</text>
  <text x="58" y="8" font-size="7" fill="var(--dt)">May</text>
  <text x="72" y="8" font-size="7" fill="var(--dt)">Jun</text>
  <text x="86" y="8" font-size="7" fill="var(--dt)">Jul</text>
  <text x="100" y="8" font-size="7" fill="var(--dt)">Aug</text>
  <text x="114" y="8" font-size="7" fill="var(--dt)">Sep</text>
  <text x="128" y="8" font-size="7" fill="var(--dt)">Oct</text>
  <text x="142" y="8" font-size="7" fill="var(--dt)">Nov</text>
  <text x="156" y="8" font-size="7" fill="var(--dt)">Dec</text>

  <!-- 星期标签列 -->
  <text x="2" y="18" font-size="6" fill="var(--dt)">Mon</text>
  <text x="2" y="30" font-size="6" fill="var(--dt)">Wed</text>
  <text x="2" y="42" font-size="6" fill="var(--dt)">Fri</text>

  <!-- 热力方块网格（示例：全年 52 周×7 天简化为 12 列×5 行） -->
  <!-- 色阶说明：#1e293b=无 #334155=低 #475569=中低 #64748b=中 #94a3b8=中高 #cbd5e1=高 #e2e8f0=极高 -->

  <!-- 第 1 行（1 月 -2 月） -->
  <rect x="12" y="20" width="5" height="5" rx="1" fill="#334155"/>
  <rect x="18" y="20" width="5" height="5" rx="1" fill="#475569"/>
  <rect x="24" y="20" width="5" height="5" rx="1" fill="#1e293b"/>
  <rect x="30" y="20" width="5" height="5" rx="1" fill="#64748b"/>
  <rect x="36" y="20" width="5" height="5" rx="1" fill="#94a3b8"/>
  <rect x="42" y="20" width="5" height="5" rx="1" fill="#cbd5e1"/>
  <rect x="48" y="20" width="5" height="5" rx="1" fill="#e2e8f0"/>
  <rect x="54" y="20" width="5" height="5" rx="1" fill="#475569"/>
  <rect x="60" y="20" width="5" height="5" rx="1" fill="#64748b"/>
  <rect x="66" y="20" width="5" height="5" rx="1" fill="#334155"/>
  <rect x="72" y="20" width="5" height="5" rx="1" fill="#94a3b8"/>
  <rect x="78" y="20" width="5" height="5" rx="1" fill="#cbd5e1"/>

  <!-- 第 2 行（3 月 -4 月） -->
  <rect x="12" y="28" width="5" height="5" rx="1" fill="#64748b"/>
  <rect x="18" y="28" width="5" height="5" rx="1" fill="#94a3b8"/>
  <rect x="24" y="28" width="5" height="5" rx="1" fill="#cbd5e1"/>
  <rect x="30" y="28" width="5" height="5" rx="1" fill="#e2e8f0"/>
  <rect x="36" y="28" width="5" height="5" rx="1" fill="#475569"/>
  <rect x="42" y="28" width="5" height="5" rx="1" fill="#64748b"/>
  <rect x="48" y="28" width="5" height="5" rx="1" fill="#334155"/>
  <rect x="54" y="28" width="5" height="5" rx="1" fill="#94a3b8"/>
  <rect x="60" y="28" width="5" height="5" rx="1" fill="#cbd5e1"/>
  <rect x="66" y="28" width="5" height="5" rx="1" fill="#e2e8f0"/>
  <rect x="72" y="28" width="5" height="5" rx="1" fill="#1e293b"/>
  <rect x="78" y="28" width="5" height="5" rx="1" fill="#475569"/>

  <!-- 第 3 行（5 月 -6 月） -->
  <rect x="12" y="36" width="5" height="5" rx="1" fill="#94a3b8"/>
  <rect x="18" y="36" width="5" height="5" rx="1" fill="#cbd5e1"/>
  <rect x="24" y="36" width="5" height="5" rx="1" fill="#e2e8f0"/>
  <rect x="30" y="36" width="5" height="5" rx="1" fill="#334155"/>
  <rect x="36" y="36" width="5" height="5" rx="1" fill="#475569"/>
  <rect x="42" y="36" width="5" height="5" rx="1" fill="#64748b"/>
  <rect x="48" y="36" width="5" height="5" rx="1" fill="#94a3b8"/>
  <rect x="54" y="36" width="5" height="5" rx="1" fill="#cbd5e1"/>
  <rect x="60" y="36" width="5" height="5" rx="1" fill="#1e293b"/>
  <rect x="66" y="36" width="5" height="5" rx="1" fill="#334155"/>
  <rect x="72" y="36" width="5" height="5" rx="1" fill="#475569"/>
  <rect x="78" y="36" width="5" height="5" rx="1" fill="#64748b"/>

  <!-- 第 4 行（7 月 -8 月） -->
  <rect x="12" y="44" width="5" height="5" rx="1" fill="#cbd5e1"/>
  <rect x="18" y="44" width="5" height="5" rx="1" fill="#e2e8f0"/>
  <rect x="24" y="44" width="5" height="5" rx="1" fill="#1e293b"/>
  <rect x="30" y="44" width="5" height="5" rx="1" fill="#334155"/>
  <rect x="36" y="44" width="5" height="5" rx="1" fill="#475569"/>
  <rect x="42" y="44" width="5" height="5" rx="1" fill="#64748b"/>
  <rect x="48" y="44" width="5" height="5" rx="1" fill="#94a3b8"/>
  <rect x="54" y="44" width="5" height="5" rx="1" fill="#cbd5e1"/>
  <rect x="60" y="44" width="5" height="5" rx="1" fill="#e2e8f0"/>
  <rect x="66" y="44" width="5" height="5" rx="1" fill="#94a3b8"/>
  <rect x="72" y="44" width="5" height="5" rx="1" fill="#64748b"/>
  <rect x="78" y="44" width="5" height="5" rx="1" fill="#475569"/>

  <!-- 第 5 行（9 月 -12 月简化） -->
  <rect x="12" y="52" width="5" height="5" rx="1" fill="#e2e8f0"/>
  <rect x="18" y="52" width="5" height="5" rx="1" fill="#cbd5e1"/>
  <rect x="24" y="52" width="5" height="5" rx="1" fill="#94a3b8"/>
  <rect x="30" y="52" width="5" height="5" rx="1" fill="#64748b"/>
  <rect x="36" y="52" width="5" height="5" rx="1" fill="#475569"/>
  <rect x="42" y="52" width="5" height="5" rx="1" fill="#334155"/>
  <rect x="48" y="52" width="5" height="5" rx="1" fill="#1e293b"/>
  <rect x="54" y="52" width="5" height="5" rx="1" fill="#475569"/>
  <rect x="60" y="52" width="5" height="5" rx="1" fill="#64748b"/>
  <rect x="66" y="52" width="5" height="5" rx="1" fill="#94a3b8"/>
  <rect x="72" y="52" width="5" height="5" rx="1" fill="#cbd5e1"/>
  <rect x="78" y="52" width="5" height="5" rx="1" fill="#e2e8f0"/>

  <!-- 右侧汇总数字 -->
  <text x="95" y="30" font-size="16" font-weight="800" fill="var(--t)">256</text>
  <text x="95" y="42" font-size="8" fill="var(--dt)">全年总数</text>

  <!-- 图例（色阶说明） -->
  <rect x="95" y="55" width="8" height="8" rx="1" fill="#1e293b"/>
  <text x="106" y="62" font-size="7" fill="var(--dt)">0</text>
  <rect x="115" y="55" width="8" height="8" rx="1" fill="#64748b"/>
  <text x="126" y="62" font-size="7" fill="var(--dt)">10</text>
  <rect x="135" y="55" width="8" height="8" rx="1" fill="#cbd5e1"/>
  <text x="146" y="62" font-size="7" fill="var(--dt)">25</text>
  <rect x="155" y="55" width="8" height="8" rx="1" fill="#e2e8f0"/>
  <text x="166" y="62" font-size="7" fill="var(--dt)">50+</text>

  <!-- 底部统计 -->
  <text x="95" y="80" font-size="8" fill="var(--dt)">日均：</text>
  <text x="120" y="80" font-size="10" font-weight="700" fill="var(--t)">7.2</text>
  <text x="95" y="92" font-size="8" fill="var(--dt)">峰值：</text>
  <text x="120" y="92" font-size="10" font-weight="700" fill="var(--gold)">23</text>
</svg>
```

**尺寸计算：**
```
全年视图：12 月×5 行（简化周）或 52 列×7 行（完整周）
简化版：每列代表 1 个月，每行代表一周
方块尺寸：5×5px 或 6×6px，间距 1px

色阶分级（5-7 级）：
0         → #1e293b（最深，无活动）
1-10      → #334155 ~ #475569（低）
11-25     → #64748b ~ #94a3b8（中）
26-40     → #cbd5e1（高）
41+       → #e2e8f0（极高）
```

**变体用法：**
```
- 月视图：31 列×1 行，显示单月每日分布
- 季度视图：90 列×1 行 或 12 列×7 行
- 周视图：7 列×24 行（每小时）
- GitHub 风格：52 周×7 天，横向排列
```
