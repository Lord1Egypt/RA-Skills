## 目标信息源地图范本

### 场景描述
从目标人物的最小识别信息（姓名+已知平台账号）出发，发现所有公开信息源，生成优先级排序。

### 输入条件
- D1-01 已确认目标唯一身份
- 已知初始信息：姓名、1+个已知平台账号

### 产出格式
信息源地图表格 + 优先级排序

### 范本内容

#### 目标信息源地图

**目标**: 张XX（已知GitHub: zhang-xx, LinkedIn: zhang-xx-linkedin）

---

**社交媒体源**

| 平台 | 账号 | URL | 信息密度 | 可达性 | 备注 |
|------|------|-----|---------|--------|------|
| 微博 | zhang_xx_real | https://weibo.com/u/xxxx | 高 | 公开 | 活跃发帖，每日更新 |
| 知乎 | 张XX | https://zhihu.com/people/xxxx | 高 | 公开 | 技术回答为主 |
| Twitter | @zhangxx_dev | https://twitter.com/xxxx | 中 | 公开 | 转发技术内容为主 |
| 小红书 | zhangxx_life | https://xiaohongshu.com/xxxx | 中 | 公开 | 生活分享 |

**职业平台源**

| 平台 | 账号 | URL | 信息密度 | 可达性 | 备注 |
|------|------|-----|---------|--------|------|
| LinkedIn | zhang-xx-linkedin | https://linkedin.com/in/xxxx | 高 | 需登录 | 完整职业履历 |
| 脉脉 | 张XX | https://maimai.cn/xxxx | 高 | 需登录 | 可能有薪资信息 |
| 拉勾 | zhang_xx | https://lagou.com/xxxx | 中 | 公开 | 历史求职记录 |

**技术足迹源**

| 平台 | 账号 | URL | 信息密度 | 可达性 | 备注 |
|------|------|-----|---------|--------|------|
| GitHub | zhang-xx | https://github.com/zhang-xx | 高 | 公开 | 50+仓库，活跃贡献 |
| Stack Overflow | zhangxx | https://stackoverflow.com/xxxx | 中 | 公开 | 技术问答 |
| 掘金 | 张XX | https://juejin.cn/user/xxxx | 中 | 公开 | 技术博客 |
| CSDN | zhang_xx_csdn | https://blog.csdn.net/xxxx | 中 | 公开 | 技术博客 |

**公开记录源**（如适用）

| 平台 | 账号 | URL | 信息密度 | 可达性 | 备注 |
|------|------|-----|---------|--------|------|
| 天眼查 | - | https://tianyancha.com/xxxx | 低 | 公开 | 如有企业关联 |
| 知网 | 张XX | https://kns.cnki.net/xxxx | 中 | 公开 | 如有发表论文 |

---

#### 优先级排序矩阵

| 优先级 | 平台 | 信息密度 | 可信度 | 覆盖维度 | 收集策略 |
|--------|------|---------|--------|---------|---------|
| P0 | LinkedIn | 高 | 高 | 维1,2,10 | 优先收集 |
| P0 | GitHub | 高 | 高 | 维1,9,10,12 | 优先收集 |
| P1 | 知乎 | 高 | 中 | 维3,6,9,11 | 次优先 |
| P1 | 微博 | 高 | 中 | 维5,6,7,11,12 | 次优先 |
| P1 | 脉脉 | 高 | 中 | 维1,2,8 | 如需登录则降级 |
| P2 | Twitter | 中 | 中 | 维6,7 | 补充收集 |
| P2 | 掘金 | 中 | 中 | 维1,10 | 补充收集 |
| P3 | 小红书 | 中 | 低 | 维5,6 | 可选收集 |
