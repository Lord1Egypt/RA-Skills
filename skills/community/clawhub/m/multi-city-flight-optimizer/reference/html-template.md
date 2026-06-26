# HTML 可视化方案对比模板

本文档定义了航线比价方案的 HTML 可视化文件模板。

## 目录

1. [完整 HTML 模板](#完整-html-模板)
2. [样式说明](#样式说明)
3. [组件说明](#组件说明)
4. [使用方法](#使用方法)

---

## 完整 HTML 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>航线比价 | {{出发城市}} ↔ {{区域}} | {{日期区间}}</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
      background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
      min-height: 100vh;
      padding: 20px;
    }
    
    .container {
      max-width: 900px;
      margin: 0 auto;
      background: #fff;
      border-radius: 20px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
      overflow: hidden;
    }
    
    /* 头部区域 */
    .header {
      background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
      color: white;
      padding: 40px 30px;
      text-align: center;
    }
    
    .header h1 {
      font-size: 2.2em;
      margin-bottom: 10px;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header .meta {
      font-size: 1.1em;
      opacity: 0.9;
    }
    
    .header .subtitle {
      margin-top: 15px;
      font-size: 0.9em;
      opacity: 0.7;
    }
    
    /* 约束摘要 */
    .constraints {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 0;
      background: #f8f9fa;
      border-bottom: 1px solid #eee;
    }
    
    .constraints .item {
      padding: 18px;
      text-align: center;
      border-right: 1px solid #eee;
    }
    
    .constraints .item:last-child { border-right: none; }
    .constraints .icon { font-size: 1.5em; margin-bottom: 5px; }
    .constraints .label { font-size: 0.8em; color: #666; }
    .constraints .value { font-size: 1em; font-weight: 600; color: #333; }
    
    /* 主体内容 */
    .content { padding: 30px; }
    
    /* 方案卡片 */
    .plan-card {
      border-radius: 16px;
      margin-bottom: 25px;
      overflow: hidden;
      box-shadow: 0 5px 20px rgba(0,0,0,0.08);
      border: 1px solid #eee;
    }
    
    .plan-header {
      padding: 18px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: white;
    }
    
    .plan-header h3 { font-size: 1.2em; }
    .plan-badge {
      background: rgba(255,255,255,0.25);
      padding: 5px 14px;
      border-radius: 20px;
      font-size: 0.85em;
      font-weight: 600;
    }
    
    .plan-1 .plan-header { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
    .plan-2 .plan-header { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
    .plan-3 .plan-header { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
    
    .plan-body { padding: 24px; }
    
    /* 航班信息 */
    .flight-section {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 20px;
    }
    
    .flight-box {
      background: #f8f9fa;
      border-radius: 12px;
      padding: 18px;
    }
    
    .flight-label {
      font-size: 0.85em;
      color: #666;
      margin-bottom: 10px;
      font-weight: 600;
    }
    
    .flight-route {
      font-size: 1.1em;
      font-weight: 700;
      color: #333;
      margin-bottom: 6px;
    }
    
    .flight-detail {
      font-size: 0.9em;
      color: #555;
      line-height: 1.6;
    }
    
    .flight-price {
      font-size: 1.3em;
      font-weight: 700;
      color: #e74c3c;
      margin-top: 8px;
    }
    
    /* 方案总结 */
    .plan-summary {
      background: #f0f4ff;
      border-radius: 12px;
      padding: 18px;
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 15px;
      text-align: center;
    }
    
    .summary-item .summary-label {
      font-size: 0.8em;
      color: #666;
      margin-bottom: 4px;
    }
    
    .summary-item .summary-value {
      font-size: 1.2em;
      font-weight: 700;
      color: #333;
    }
    
    .summary-item .summary-value.price { color: #e74c3c; }
    
    /* 方案理由 */
    .plan-reason {
      margin-top: 15px;
      padding: 12px 18px;
      background: #fff8e1;
      border-radius: 10px;
      font-size: 0.9em;
      color: #856404;
      line-height: 1.6;
    }
    
    /* 方案差异标注 */
    .plan-diff {
      margin-top: 12px;
      padding: 10px 18px;
      background: #e8f5e9;
      border-radius: 10px;
      font-size: 0.85em;
      color: #2e7d32;
    }
    
    .plan-diff.warn {
      background: #fff3e0;
      color: #e65100;
    }
    
    /* 预订按钮 */
    .book-links {
      display: flex;
      gap: 10px;
      margin-top: 15px;
    }
    
    .book-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 10px 18px;
      border-radius: 25px;
      text-decoration: none;
      font-weight: 600;
      font-size: 0.9em;
      transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .book-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 5px 15px rgba(0,0,0,0.15);
    }
    
    .book-btn.primary {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
    }
    
    .book-btn.secondary {
      background: #f0f0f0;
      color: #333;
    }
    
    /* 对比表格 */
    .compare-card {
      background: #f8f9fa;
      border-radius: 16px;
      padding: 25px;
      margin: 30px 0;
    }
    
    .compare-card h2 {
      font-size: 1.2em;
      margin-bottom: 20px;
      color: #333;
    }
    
    .compare-table {
      width: 100%;
      border-collapse: collapse;
      background: white;
      border-radius: 10px;
      overflow: hidden;
    }
    
    .compare-table th {
      background: #2c5364;
      color: white;
      padding: 14px;
      text-align: center;
      font-size: 0.9em;
    }
    
    .compare-table td {
      padding: 14px;
      text-align: center;
      border-bottom: 1px solid #eee;
      font-size: 0.9em;
    }
    
    .compare-table tr:last-child td { border-bottom: none; }
    .compare-table tr:nth-child(even) { background: #f8f9fa; }
    
    .highlight { font-weight: 700; color: #e74c3c; }
    .tag-best { background: #fce4ec; color: #c62828; padding: 3px 10px; border-radius: 10px; font-size: 0.8em; }
    .tag-cheap { background: #e3f2fd; color: #1565c0; padding: 3px 10px; border-radius: 10px; font-size: 0.8em; }
    .tag-fast { background: #e8f5e9; color: #2e7d32; padding: 3px 10px; border-radius: 10px; font-size: 0.8em; }
    
    /* 可玩性建议 */
    .route-card {
      background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
      border-radius: 16px;
      padding: 25px;
      margin: 30px 0;
    }
    
    .route-card h2 {
      font-size: 1.2em;
      margin-bottom: 15px;
      color: #333;
    }
    
    .route-flow {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 15px;
      margin: 20px 0;
      flex-wrap: wrap;
    }
    
    .route-city {
      background: white;
      padding: 10px 20px;
      border-radius: 25px;
      font-weight: 600;
      box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    
    .route-arrow {
      color: #666;
      font-size: 1.2em;
    }
    
    .route-transport {
      font-size: 0.85em;
      color: #555;
      text-align: center;
      line-height: 1.8;
      margin-top: 15px;
    }
    
    /* 提醒卡片 */
    .tips-card {
      background: #fff3cd;
      border-radius: 16px;
      padding: 25px;
      margin: 30px 0;
    }
    
    .tips-card h2 {
      font-size: 1.2em;
      margin-bottom: 15px;
      color: #856404;
    }
    
    .tips-list {
      list-style: none;
    }
    
    .tips-list li {
      padding: 8px 0;
      padding-left: 25px;
      position: relative;
      color: #856404;
      line-height: 1.6;
    }
    
    .tips-list li::before {
      content: '💡';
      position: absolute;
      left: 0;
    }
    
    /* 页脚 */
    .footer {
      text-align: center;
      padding: 30px;
      background: #f8f9fa;
      color: #666;
      font-size: 0.85em;
    }
    
    /* 响应式 */
    @media (max-width: 600px) {
      body { padding: 10px; }
      .header { padding: 30px 20px; }
      .header h1 { font-size: 1.6em; }
      .constraints { grid-template-columns: repeat(2, 1fr); }
      .constraints .item { border-bottom: 1px solid #eee; }
      .content { padding: 20px; }
      .flight-section { grid-template-columns: 1fr; }
      .plan-summary { grid-template-columns: 1fr; }
      .route-flow { flex-direction: column; }
    }
    
    /* 打印样式 */
    @media print {
      body { background: white; padding: 0; }
      .container { box-shadow: none; }
      .book-btn { display: none; }
    }
  </style>
</head>
<body>
  <div class="container">
    <!-- 头部 -->
    <div class="header">
      <h1>✈️ 航线比价方案</h1>
      <div class="meta">{{出发城市}} ↔ {{区域}}多城 · {{日期区间}}</div>
      <div class="subtitle">{{候选城市列表}} · 共{{组合数}}种组合 · 已筛出 Top 3</div>
    </div>
    
    <!-- 约束摘要 -->
    <div class="constraints">
      <div class="item">
        <div class="icon">📍</div>
        <div class="label">出发城市</div>
        <div class="value">{{出发城市}}</div>
      </div>
      <div class="item">
        <div class="icon">📅</div>
        <div class="label">假期范围</div>
        <div class="value">{{日期区间}}</div>
      </div>
      <div class="item">
        <div class="icon">👥</div>
        <div class="label">出行人数</div>
        <div class="value">{{人数}}人</div>
      </div>
      <div class="item">
        <div class="icon">🎯</div>
        <div class="label">优化偏好</div>
        <div class="value">{{偏好}}</div>
      </div>
    </div>
    
    <div class="content">
      
      <!-- 方案1：综合最优 -->
      <div class="plan-card plan-1">
        <div class="plan-header">
          <h3>🥇 方案1</h3>
          <span class="plan-badge">综合最优</span>
        </div>
        <div class="plan-body">
          <div class="flight-section">
            <div class="flight-box">
              <div class="flight-label">✈️ 去程</div>
              <div class="flight-route">{{出发城市}} → {{方案1去程城市}}</div>
              <div class="flight-detail">
                {{方案1去程日期}} · {{方案1去程航班号}}<br>
                {{方案1去程时间}} · {{方案1去程航空公司}}<br>
                中转{{方案1去程中转次数}}次（{{方案1去程中转城市}}）· 总飞行{{方案1去程总时长}}
              </div>
              <div class="flight-price">¥{{方案1去程价格}}/人</div>
            </div>
            <div class="flight-box">
              <div class="flight-label">✈️ 回程</div>
              <div class="flight-route">{{方案1回程城市}} → {{出发城市}}</div>
              <div class="flight-detail">
                {{方案1回程日期}} · {{方案1回程航班号}}<br>
                {{方案1回程时间}} · {{方案1回程航空公司}}<br>
                中转{{方案1回程中转次数}}次（{{方案1回程中转城市}}）· 总飞行{{方案1回程总时长}}
              </div>
              <div class="flight-price">¥{{方案1回程价格}}/人</div>
            </div>
          </div>
          
          <div class="plan-summary">
            <div class="summary-item">
              <div class="summary-label">💰 往返总价/人</div>
              <div class="summary-value price">¥{{方案1总价}}</div>
            </div>
            <div class="summary-item">
              <div class="summary-label">⏱️ 总飞行时长</div>
              <div class="summary-value">{{方案1总飞行时长}}</div>
            </div>
            <div class="summary-item">
              <div class="summary-label">🔄 总中转次数</div>
              <div class="summary-value">{{方案1总中转}}次</div>
            </div>
          </div>
          
          <div class="plan-reason">
            💡 {{方案1理由}}
          </div>
          
          <div class="book-links">
            <a href="{{方案1去程jumpUrl}}" class="book-btn primary" target="_blank">✈️ 预订去程</a>
            <a href="{{方案1回程jumpUrl}}" class="book-btn primary" target="_blank">✈️ 预订回程</a>
          </div>
        </div>
      </div>
      
      <!-- 方案2：更省钱 -->
      <div class="plan-card plan-2">
        <div class="plan-header">
          <h3>🥈 方案2</h3>
          <span class="plan-badge">更省钱</span>
        </div>
        <div class="plan-body">
          <div class="flight-section">
            <div class="flight-box">
              <div class="flight-label">✈️ 去程</div>
              <div class="flight-route">{{出发城市}} → {{方案2去程城市}}</div>
              <div class="flight-detail">
                {{方案2去程日期}} · {{方案2去程航班号}}<br>
                {{方案2去程时间}} · 中转{{方案2去程中转次数}}次 · 总飞行{{方案2去程总时长}}
              </div>
              <div class="flight-price">¥{{方案2去程价格}}/人</div>
            </div>
            <div class="flight-box">
              <div class="flight-label">✈️ 回程</div>
              <div class="flight-route">{{方案2回程城市}} → {{出发城市}}</div>
              <div class="flight-detail">
                {{方案2回程日期}} · {{方案2回程航班号}}<br>
                {{方案2回程时间}} · 中转{{方案2回程中转次数}}次 · 总飞行{{方案2回程总时长}}
              </div>
              <div class="flight-price">¥{{方案2回程价格}}/人</div>
            </div>
          </div>
          
          <div class="plan-summary">
            <div class="summary-item">
              <div class="summary-label">💰 往返总价/人</div>
              <div class="summary-value price">¥{{方案2总价}}</div>
            </div>
            <div class="summary-item">
              <div class="summary-label">⏱️ 总飞行时长</div>
              <div class="summary-value">{{方案2总飞行时长}}</div>
            </div>
            <div class="summary-item">
              <div class="summary-label">🔄 总中转次数</div>
              <div class="summary-value">{{方案2总中转}}次</div>
            </div>
          </div>
          
          <div class="plan-diff">
            📉 比方案1便宜 ¥{{方案2省钱差额}}/人
          </div>
          <div class="plan-diff warn">
            ⚠️ 代价：{{方案2代价说明}}
          </div>
          
          <div class="book-links">
            <a href="{{方案2去程jumpUrl}}" class="book-btn primary" target="_blank">✈️ 预订去程</a>
            <a href="{{方案2回程jumpUrl}}" class="book-btn primary" target="_blank">✈️ 预订回程</a>
          </div>
        </div>
      </div>
      
      <!-- 方案3：更省时/更稳 -->
      <div class="plan-card plan-3">
        <div class="plan-header">
          <h3>🥉 方案3</h3>
          <span class="plan-badge">更省时 / 更稳</span>
        </div>
        <div class="plan-body">
          <div class="flight-section">
            <div class="flight-box">
              <div class="flight-label">✈️ 去程</div>
              <div class="flight-route">{{出发城市}} → {{方案3去程城市}}</div>
              <div class="flight-detail">
                {{方案3去程日期}} · {{方案3去程航班号}}<br>
                {{方案3去程时间}} · 中转{{方案3去程中转次数}}次 · 总飞行{{方案3去程总时长}}
              </div>
              <div class="flight-price">¥{{方案3去程价格}}/人</div>
            </div>
            <div class="flight-box">
              <div class="flight-label">✈️ 回程</div>
              <div class="flight-route">{{方案3回程城市}} → {{出发城市}}</div>
              <div class="flight-detail">
                {{方案3回程日期}} · {{方案3回程航班号}}<br>
                {{方案3回程时间}} · 中转{{方案3回程中转次数}}次 · 总飞行{{方案3回程总时长}}
              </div>
              <div class="flight-price">¥{{方案3回程价格}}/人</div>
            </div>
          </div>
          
          <div class="plan-summary">
            <div class="summary-item">
              <div class="summary-label">💰 往返总价/人</div>
              <div class="summary-value price">¥{{方案3总价}}</div>
            </div>
            <div class="summary-item">
              <div class="summary-label">⏱️ 总飞行时长</div>
              <div class="summary-value">{{方案3总飞行时长}}</div>
            </div>
            <div class="summary-item">
              <div class="summary-label">🔄 总中转次数</div>
              <div class="summary-value">{{方案3总中转}}次</div>
            </div>
          </div>
          
          <div class="plan-diff">
            ⏱️ 比方案1省 {{方案3省时差额}} 飞行 / 少 {{方案3少中转}} 次中转
          </div>
          <div class="plan-diff warn">
            ⚠️ 代价：{{方案3代价说明}}
          </div>
          
          <div class="book-links">
            <a href="{{方案3去程jumpUrl}}" class="book-btn primary" target="_blank">✈️ 预订去程</a>
            <a href="{{方案3回程jumpUrl}}" class="book-btn primary" target="_blank">✈️ 预订回程</a>
          </div>
        </div>
      </div>
      
      <!-- 对比表格 -->
      <div class="compare-card">
        <h2>📊 三方案速览对比</h2>
        <table class="compare-table">
          <thead>
            <tr>
              <th></th>
              <th>去→回</th>
              <th>往返总价/人</th>
              <th>总飞行</th>
              <th>总中转</th>
              <th>标签</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>🥇</td>
              <td>{{方案1去程城市}}→{{方案1回程城市}}回</td>
              <td class="highlight">¥{{方案1总价}}</td>
              <td>{{方案1总飞行时长}}</td>
              <td>{{方案1总中转}}次</td>
              <td><span class="tag-best">综合最优</span></td>
            </tr>
            <tr>
              <td>🥈</td>
              <td>{{方案2去程城市}}→{{方案2回程城市}}回</td>
              <td class="highlight">¥{{方案2总价}}</td>
              <td>{{方案2总飞行时长}}</td>
              <td>{{方案2总中转}}次</td>
              <td><span class="tag-cheap">更省钱</span></td>
            </tr>
            <tr>
              <td>🥉</td>
              <td>{{方案3去程城市}}→{{方案3回程城市}}回</td>
              <td class="highlight">¥{{方案3总价}}</td>
              <td>{{方案3总飞行时长}}</td>
              <td>{{方案3总中转}}次</td>
              <td><span class="tag-fast">更省时</span></td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- 可玩性建议 -->
      <div class="route-card">
        <h2>🗺️ 可玩性路线建议（基于方案1）</h2>
        
        <div class="route-flow">
          <div class="route-city">✈️ {{方案1去程城市}}</div>
          <div class="route-arrow">→</div>
          <div class="route-city">{{中间城市1}}</div>
          <div class="route-arrow">→</div>
          <div class="route-city">{{方案1回程城市}} ✈️</div>
        </div>
        
        <div class="route-transport">
          {{城际交通说明1}}<br>
          {{城际交通说明2}}<br>
          💡 {{路线建议一句话}}
        </div>
      </div>
      
      <!-- 提醒 -->
      <div class="tips-card">
        <h2>‼️ 重要提醒</h2>
        <ul class="tips-list">
          <li>机票价格实时波动，以上为当前搜索结果，建议尽快预订锁定价格</li>
          <li>{{签证提醒}}</li>
          <li>{{季节/天气提醒}}</li>
          <li>{{其他提醒}}</li>
        </ul>
      </div>
      
    </div>
    
    <!-- 页脚 -->
    <div class="footer">
      <p>由 FlyAI 航线比价助手生成 · {{生成时间}}</p>
      <p>数据来源：飞猪旅行 · 价格仅供参考</p>
    </div>
  </div>
</body>
</html>
```

---

## 样式说明

### 配色方案

| 元素 | 颜色 | 用途 |
|------|------|------|
| 主色调 | `#0f2027 → #203a43 → #2c5364` | 头部、深色调背景 |
| 方案1 | `#f093fb → #f5576c` | 综合最优，粉红系 |
| 方案2 | `#4facfe → #00f2fe` | 更省钱，蓝色系 |
| 方案3 | `#43e97b → #38f9d7` | 更省时，绿色系 |
| 路线建议 | `#ffecd2 → #fcb69f` | 暖色，柔和 |
| 提醒 | `#fff3cd` | 黄色警告 |
| 价格高亮 | `#e74c3c` | 红色，醒目 |

### 响应式断点

- **桌面端**：> 600px，双栏航班信息
- **移动端**：≤ 600px，单栏布局

---

## 组件说明

### 1. 头部区域 (header)
展示"航线比价方案"标题、出发地↔区域、候选城市列表

### 2. 约束摘要 (constraints)
4格快速预览：出发城市、假期范围、人数、优化偏好

### 3. 方案卡片 (plan-card)
- plan-header：方案标题 + 标签（综合最优/更省钱/更省时）
- flight-section：去程/回程双栏航班信息
- plan-summary：3格摘要（总价/总飞行/总中转）
- plan-reason：一句话推荐理由
- plan-diff：与方案1的差异说明
- book-links：飞猪预订按钮

### 4. 对比表格 (compare-card)
三方案横向对比表

### 5. 路线建议 (route-card)
可视化城市顺序流 + 城际交通说明

### 6. 提醒 (tips-card)
价格波动、签证、天气等提醒

---

## 使用方法

### 生成 HTML 文件

1. 完成所有航线搜索和评分
2. 替换模板中的 `{{变量}}` 占位符
3. 使用 `create_file` 工具生成文件

### 核心变量列表

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{出发城市}}` | 用户出发城市 | 杭州 |
| `{{区域}}` | 目的地区域 | 南欧 |
| `{{日期区间}}` | 假期范围 | 10.1-10.7 |
| `{{候选城市列表}}` | 所有候选城市 | 巴塞罗那 · 马德里 · 里斯本 |
| `{{组合数}}` | 评估的组合总数 | 9 |
| `{{人数}}` | 出行人数 | 2 |
| `{{偏好}}` | 用户偏好 | 综合最优 |
| `{{方案N去程城市}}` | 方案N的去程到达城市 | 巴塞罗那 |
| `{{方案N回程城市}}` | 方案N的回程出发城市 | 里斯本 |
| `{{方案N总价}}` | 方案N的往返总价/人 | 5,280 |
| `{{方案N总飞行时长}}` | 方案N的总飞行时长 | 28h |
| `{{方案N总中转}}` | 方案N的总中转次数 | 2 |
| `{{方案N理由}}` | 方案N的推荐理由 | 价格适中... |
| `{{方案N去程jumpUrl}}` | 去程飞猪预订链接 | https://... |
| `{{方案N回程jumpUrl}}` | 回程飞猪预订链接 | https://... |
| `{{生成时间}}` | 方案生成时间 | 2026-03-31 |
