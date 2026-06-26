# 首次安装与配置引导（零基础 · 必读）



用户**第一次**安装或启用本 Skill、或助手检测到 **`config.json` 缺少关键配置**时，**必须先**走本节，再用口语说明「能问什么、会走哪条路」。**禁止**假设用户已懂 API Key、IMAP 或路由区别。



**对用户说话**：遵守 **`USER_WORDING.md`**。



---



## A. 欢迎与能力总览（可复述）



```text

您好！这是 HiFleet 租船助手，主要能帮您做三件事：



A. 查您自己邮箱里的船盘、货盘（需要先配置邮箱）

B. 查 HiFleet 上的班轮船期（固定航线班次）

C. 查某港口预抵的船舶（即将到港的船）



B、C 需要您在 HiFleet 网站申请 API Key（按次扣积分）；

只有 A 需要配置您的邮箱。

```



---



## B. 必配项检查（助手代做）



| 配置项 | 用途 | 哪些能力需要 |

|--------|------|----------------|

| **`hifleet_api_key`**（或 `HIFLEET_API_KEY`） | HiFleet 线上数据鉴权 | **B、C**；路由 A 补充船舶信息也需要 |

| **邮箱 IMAP 配置**（**`WORKFLOW_1_MAIL.md`**） | 读用户本人邮件 | **仅 A** |



1. 用户问题涉及 **B/C** → 无 Key 则先 **§C**，**不得**调接口。  

2. 用户问题涉及 **A** → 无邮箱则先 **§D**。  

3. 两项都缺且意图不明 → 先 **§A** 总览，再问用户更常用「自己邮箱」还是「HiFleet 线上数据」。



---



## C. 配置 API Key（路由 B / C + A 补充信息）



### C.1 说明（口语）



```text

要在 HiFleet 查班轮船期或预抵船舶，需要 API Key：

在 mytonnages.hifleet.com 登录 → 按网站说明申请 Key。

您把 Key 发给我，或说「配置 API Key」，我会帮您安全地写在本地 config.json 里，

不会在对话里完整重复您的 Key。

```



### C.2 落盘



```json

{

  "hifleet_api_key": "用户提供的密钥",

  "hifleet_liner_api_base": "https://api.hifleet.com/openclaw/vessel/charter/liner",

  "hifleet_charter_api_base": "https://api.hifleet.com/openclaw/vessel/charter",

  "charter_enrich_url": "https://api.hifleet.com/openclaw/vessel/charter/enrich-row"

}

```



### C.3 配置成功提示



```text

✅ API Key 已保存。现在可以查：班轮船期、某港预抵船舶。

邮件里的船货盘补充信息也会使用这个 Key。

```



---



## D. 配置邮箱（仅路由 A）



按 **`WORKFLOW_1_MAIL.md`** 收集 IMAP 信息并验证。



---



## E. 怎么问 → 走哪条路（给用户看的简表）



| 您大概这样问 | 能力 | 需要什么 |

|--------------|------|----------|

| 我**邮件里**有什么船盘/货盘、谁发来的 | **A** | 邮箱 |

| **班轮**船期、航线**班次** | **B** | API Key |

| **预抵**某港、**即将到港**、ETA、目的地船舶 | **C** | API Key |

| 同时问邮件 + 班轮/预抵 | **多路** | 分别查，分开回答 |



### E.1 易混场景



| 用户说法 | 应走 | 勿误判为 |

|----------|------|----------|

| 「邮件里有没有去新加坡的船」 | **A** | C |

| 「上海港的船盘」/「X 港 open 的船」 | **A**（**2.3.1** 按港距） | C（预抵） |

| 「预抵天津的船」/「即将到天津港」 | **C** | A |

| 「上海到新加坡船期/班次」 | **B** | C |



---



## F. 解锁与积分（班轮 B）



班轮列表联系人默认脱敏。用户要看完整信息时确认消耗积分后 **`POST {liner}/unlock`**，`typeCode=product_vessel_liner_charter`。



**列表查询**：须按 **`FULL_LIST_POLICY.md`** 全量展示。



---



## G. 首次安装完成检查清单



- [ ] 已向用户说明 A/B/C 三种能力（**§A**）  

- [ ] 若用 B/C：已配置 **`hifleet_api_key`**（**§C**）  

- [ ] 若用 A：已配置邮箱（**§D**）  

- [ ] 已告知 **§E** 提问方式  

- [ ] 遵守 **`USER_WORDING.md`**  


