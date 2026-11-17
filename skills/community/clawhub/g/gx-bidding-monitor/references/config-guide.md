# 威能全平台招标信息监控任务 — 配置总表 v2.0

## 任务概述
- **任务名称**: 威能全平台招标信息监控-执行脚本
- **任务ID**: caba3057-082f-4bff-af4f-0f1df77bc617
- **创建时间**: 2026-06-17
- **重大更新**: 2026-06-21
- **执行频率**: 每日 10:23 (Asia/Shanghai)
- **执行方式**: OpenClaw Cron 定时任务
- **发送渠道**: 微信 (openclaw-weixin)

---

## 任务配置

### 定时任务参数
```json
{
  "schedule": {
    "kind": "cron",
    "expr": "23 10 * * *",
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "session:agent:main:openclaw-weixin:direct:o9cq804docucd1w6o7gtdvjqnbne@im.wechat",
  "delivery": {
    "mode": "announce",
    "channel": "openclaw-weixin",
    "to": "o9cq804DoCUcD1W6O7gtDvjQnBNE@im.wechat",
    "accountId": "bb7825bbb743-im-bot"
  }
}
```

### 执行超时
- **timeoutSeconds**: 600 (10分钟，默认扫描2-3个分类)

---

## 监控网站分类总览（50+平台）

### 分类一：政府公共资源交易中心（9个）— 全量采集

| 序号 | 地区 | 名称 | URL | 登录 |
|:---|:---|:---|:---|:---|
| 1 | 南宁 | 南宁市公共资源交易中心 | https://www.nnggzy.org.cn/gxnnzbw/default.aspx | 否 |
| 2 | 广西 | 广西壮族自治区公共资源交易中心 | http://202.103.240.162:8081/GgzyjySSO/login/oauth2login | 否 |
| 3 | 河池 | 广西河池公共资源交易中心 | http://www.hcjyxxw.com/gxhczbw/default.aspx | 否 |
| 4 | 环江 | 环江毛南族自治县电子招投标交易平台 | http://219.159.164.18:8211/TPBidder/memberLogin | 否 |
| 5 | 广西 | 全国平台(广西) | http://ggzy.jgswj.gxzf.gov.cn/gxggzy/ | 否 |
| 6 | 南宁 | 南宁交易中心 | http://ggzy.nanning.gov.cn/nnzfcg/sjcggg/index.htm | 否 |
| 7 | 柳州 | 柳州交易中心 | http://ggzy.liuzhou.gov.cn/ | 否 |
| 8 | 桂林 | 桂林交易中心 | https://ggzy.jgswj.gxzf.gov.cn/glggzy/jyxx/ | 否 |
| 9 | 玉林 | 玉林交易中心 | http://ggzy.jgswj.gxzf.gov.cn/ylggzy/jyxx/ | 否 |

### 分类二：南方电网及电力平台（5个）— 电力类筛选

| 序号 | 名称 | URL | 登录 |
|:---|:---|:---|:---|
| 1 | 中国南方电网电子商务系统 | http://www.bidding.csg.cn/ | 否 |
| 2 | 南方电网电子采购交易平台 | https://ecsg.com.cn/ | 否 |
| 3 | 电能e招采平台 | https://ebid.espic.com.cn/ | 需登录 |
| 4 | 中国华电集团电子商务平台 | https://www.chdtp.com/ | 否 |
| 5 | 大唐电子商务平台 | http://www.cdt-ec.com | 否 |

### 分类三：能源及央企平台（4个）

| 序号 | 名称 | URL | 登录 |
|:---|:---|:---|:---|
| 1 | 国家能源e购 | https://www.neep.shop/ | 需登录 |
| 2 | 国家能源招标网 | http://www.chnenergybidding.com.cn/ | 需登录 |
| 3 | 中国铁塔电子采购平台 | https://ebid.chinatowercom.cn | 否 |
| 4 | 国家网管采购管理子系统 | https://iscm.pipechina.com.cn:8443/ | 否 |

### 分类四：房地产集团招采平台（13个）

| 序号 | 名称 | URL | 登录 |
|:---|:---|:---|:---|
| 1 | 金科房地产 | https://www.jinke.com/ | 否 |
| 2 | 彰泰招采 | http://caigou.mingyuanyun.com/glztjt | 否 |
| 3 | 万达采招 | https://vendor.wanda.cn/ | 否 |
| 4 | 华润守正电子招标 | http://szecp.crc.com.cn/ | 否 |
| 5 | 旭辉集团 | https://supplier.cifi.com.cn/ | 否 |
| 6 | 奥园集团 | https://ayjc.aoyuan.net/ | 否 |
| 7 | 广西保利置业 | http://polygx.julytech.cn | 否 |
| 8 | 敏捷集团 | https://gys.nimble.cn:8443/ | 否 |
| 9 | 中南房地产 | http://go.zoina.cn/ | 否 |
| 10 | 建发集团 | https://supplier.cndservice.com/ | 否 |
| 11 | 联东U谷招采 | http://sup.liando.cn/ | 需登录 |
| 12 | 联东U谷-供应商 | http://gyswy.liando.cn/ | 需登录 |
| 13 | 南南铝集团 | http://oms.alnan.com:8089/ | 需登录 |

### 分类五：国企/大型集团（7个）

| 序号 | 名称 | URL | 登录 |
|:---|:---|:---|:---|
| 1 | 广西北部湾投资集团 | https://ebidding.bgigc.com/ | 否 |
| 2 | 广西交投集中采购 | http://sp.jc.gxjttz.com/ | 否 |
| 3 | 广西路桥集团 | https://client.lxyun.cn/ | 否 |
| 4 | 荣耀集团 | http://ec.gxry.cn/ | 否 |
| 5 | 广西交易所集团 | https://mh.gxcq.com.cn/ | 否 |
| 6 | 广西联合产权交易所 | https://mh.gxcq.com.cn/ | 否 |
| 7 | 广西阳光采购服务 | https://gxygcg.ejy365.com/ | 否 |

### 分类六：央企及行业平台（7个）

| 序号 | 名称 | URL | 登录 |
|:---|:---|:---|:---|
| 1 | 中国铁建供应链金融 | https://yx.crcc.cn/ | 需登录 |
| 2 | 中交招采网 | https://zjzcw.iccec.cn/ | 否 |
| 3 | 中国电建承包商管理 | https://bid.powerchina.cn/ | 需登录 |
| 4 | 中国通服采招门户 | https://szyc.chinaccs.cn/ | 否 |
| 5 | 中国融通电子商务 | https://www.ronghw.cn/ | 否 |
| 6 | 中航建设集团 | https://scm.avicjs.com/ | 否 |
| 7 | 集采履约平台 | https://scm.avicjs.com/ | 否 |

### 分类七：行业垂直平台（7个）

| 序号 | 名称 | URL | 登录 |
|:---|:---|:---|:---|
| 1 | 政采云 | https://www.zcygov.cn/ | 需登录 |
| 2 | 云筑网 | https://auth.yzw.cn/ | 需登录 |
| 3 | 标桥 | https://zhidao.bqpoint.com/ | 需登录 |
| 4 | 国铁采购平台 | https://cg.95306.cn/ | 否 |
| 5 | 精彩纵横 | https://passport.yingcaicheng.com/ | 否 |
| 6 | 京东企业 | https://wcjt.jd.com | 否 |
| 7 | 建行阳光集采 | https://ibuy.ccb.com/ | 否 |

### 分类八：其他企业采购（5个）

| 序号 | 名称 | URL | 登录 |
|:---|:---|:---|:---|
| 1 | 中国移动投标网 | https://b2b.10086.cn/ | 否 |
| 2 | 大华供应商门户 | http://cg.dahuahome.com/ | 否 |
| 3 | 南方航空采购招标 | https://csbidding.csair.cn/ | 否 |
| 4 | 武汉武钢(优必选) | https://www.obei.com.cn/ | 需登录 |
| 5 | 双胞胎集团 | https://portal.us.bn.cloud.ariba.com/ | 需登录 |

---

## 已注册登录账号台账

### 政采云
- 网址: https://www.zcygov.cn/
- 账号: WN141588
- 密码: wndl141588
- 备注: 广西政府采购核心平台

### 国家能源e购
- 网址: https://www.neep.shop/
- 用户名: 310150717
- 密码: Wndl717400!@!
- 申请人: 蓝庆武 13667716933
- 管理员: 吴珍 15994437537（验证码登录）

### 国家能源招标网
- 网址: http://www.chnenergybidding.com.cn/
- 登录名: 13667716933
- 密码: Gxwn141488.

### 云筑网
- 网址: https://auth.yzw.cn/login/v2
- 用户名: WNDL1414
- 密码: wndl141588
- 备注: 中建集团旗下

### 联东U谷招采系统
- 网址: http://sup.liando.cn/
- 登录名: GXWNDL
- 密码: wn123456
- 注册人: 曾升云
- 邮箱: 88069000@qq.com

### 广西交投宏冠
- 网址: http://jthg.zcjb.com.cn/ebidding/#/login
- 账号: 15994437537
- 密码: wndl822825!

### 中国铁建供应链金融
- 网址: https://yx.crcc.cn/
- 账号: 15994437537
- 密码: Wndl717400!

### 武汉武钢(优必选)
- 网址: https://www.obei.com.cn/
- 账号: 15994437537
- 密码: Wndl822825@

### 交建云商
- 网址: https://emp.iccec.cn/
- 账号: 15994437537
- 密码: e?Nf?U3X8

### 标桥
- 网址: https://zhidao.bqpoint.com/
- 账号: 15994437537
- 密码: WN822825

### 南南铝集团招采平台
- 网址: http://oms.alnan.com:8089/
- 用户名: 广西威能电力有限公司
- 密码: wndl8866
- 注册人: 曾升云 15278010524
- 子账号: WNDL822825（庞艳 13978962721），密码 WNDL822825!

### 电能e招采平台
- 网址: https://ebid.espic.com.cn/
- 用户名: WNDL822
- 密码: Weineng13579!
- 注册手机: 19968289744（黄宁军）
- 邮箱: 934865592@qq.com
- 电子印章: 数智签（吴珍手机），密码: 822825

### 联东U谷-供应商平台
- 网址: http://gyswy.liando.cn/suppliers-portal/
- 登录名: Wndl822
- 登录方式: 手机验证码
- 手机号: 15994437537

### 中国电建承包商管理系统
- 网址: https://bid.powerchina.cn/Contractor/register
- 账号: 广西威能电力有限公司
- 密码: Wn717400@
- 注册手机: 15994437537

### 云城建项目全过程管理系统
- 网址: http://w.cloudcj.cn/
- 账号: 吴珍
- 密码: Wndl822825
- 注册手机: 15994437537

### 中铁鲁班商务网
- 网址: https://datasrvportal.crecgec.com/
- 账号: WNDL
- 密码: WN717400！
- 注册手机: 15994437537

### 双胞胎集团
- 网址: https://portal.us.bn.cloud.ariba.com/
- 用户名: 1286039045@qq.com
- 密码: WNdl7174!
- Business Network ID: AN11245504346
- 管理员: 1286039045@qq.com（李牟彪）
- 电话: 17776309367

---

## 电力类筛选关键词

```
配电、供配电、扩容、线路、迁改、增容、一户一表、
10kV、35kV、110kV、变压器、箱变、开闭所、配电房、配电室、
电缆、电力、供电、用电、配网、电网、输变电、变电站、供电所、
充电桩、充电站、新能源、光伏、储能、风电、高压、低压、
开关柜、断路器、母线、桥架、接地、电气安装、电气工程、
电气设备、成套设备、无功补偿、防雷、计量、互感器、避雷器
```

---

## 轮换扫描机制

### 每日固定扫描（必扫）
- 政府公共资源交易中心
- 南方电网及电力平台

### 每日轮换扫描（按星期几）
- 周一: 能源央企
- 周二: 房地产集团
- 周三: 国企/大型集团
- 周四: 央企及行业平台
- 周五: 行业垂直平台
- 周六: 其他企业采购
- 周日: 综合回顾（补充遗漏）

这样确保一周覆盖所有8个分类，同时单次执行时间控制在10分钟内。

---

## 相关文件

| 文件 | 用途 | 路径 |
|------|------|------|
| **主脚本** | 执行爬取和筛选 | `skills/gx-bidding-monitor/scripts/gx_bidding_monitor.py` |
| **网站清单** | 全部50+平台配置 | `skills/gx-bidding-monitor/references/gx_websites.json` |
| **配置文档** | 本说明文件 | `skills/gx-bidding-monitor/references/config-guide.md` |
| **每日结果** | 爬取原始数据 | `bidding_results_YYYYMMDD.json` |
| **微信消息** | 每日推送内容 | `wechat_msg_YYYYMMDD.txt` |

---

## 运维命令

### 查看任务状态
```bash
openclaw cron get caba3057-082f-4bff-af4f-0f1df77bc617
```

### 手动立即运行
```bash
openclaw cron run caba3057-082f-4bff-af4f-0f1df77bc617
```

### 停用/启用任务
```bash
openclaw cron update caba3057-082f-4bff-af4f-0f1df77bc617 --enabled=false
openclaw cron update caba3057-082f-4bff-af4f-0f1df77bc617 --enabled=true
```

### 查看定时任务列表
```bash
openclaw cron list
```

### 手动执行脚本测试（默认轮换）
```bash
cd ~/.openclaw/workspace && python3 skills/gx-bidding-monitor/scripts/gx_bidding_monitor.py
```

### 扫描指定分类
```bash
python3 skills/gx-bidding-monitor/scripts/gx_bidding_monitor.py --category power_grid
```

### 扫描所有分类
```bash
python3 skills/gx-bidding-monitor/scripts/gx_bidding_monitor.py --all
```

### 查看登录平台清单
```bash
python3 skills/gx-bidding-monitor/scripts/gx_bidding_monitor.py --auth-only
```

---

## 历史记录

| 日期 | 操作 | 说明 |
|------|------|------|
| 2026-06-17 | 创建任务 | 初始配置，urllib方式，失败率高 |
| 2026-06-17 | 改用browser | 切换到browser模拟浏览器，聚焦核心10个网站 |
| 2026-06-17 | 固化任务 | 建立配置文档，更新MEMORY.md |
| 2026-06-21 | 重大升级v2.0 | 扩展至50+平台，8大分类，加入账号台账管理，轮换扫描机制 |

---

## 注意事项

1. **Browser依赖**: 脚本使用 `openclaw browser` CLI，需确保Chrome/Chromium已安装
2. **网络环境**: 政府网站偶有维护或改版，需定期检查URL有效性
3. **微信推送**: 依赖微信渠道配置，如更换微信账号需同步更新 `to` 字段
4. **执行时长**: 默认扫描2-3个分类约5-8分钟，全量扫描约20-30分钟，超时设置为10分钟
5. **历史数据**: 每日结果自动保存JSON，可按需清理或归档
6. **账号安全**: 账号密码存储在 `gx_websites.json` 中，请勿随仓库公开提交
7. **登录平台**: 当前版本不自动模拟登录，建议每日手动登录查看，脚本会在日报中提醒

---

*配置文档版本: v2.0*  
*最后更新: 2026-06-21*
