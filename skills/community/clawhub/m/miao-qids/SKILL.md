---
name: MiaoQIDS
description: "MiaoQIDS 经典-量子混合防火墙入侵检测系统技能喵～ v0.2.0（发布前暂定）。基于经典神经网络（CNN，非卷积）做特征提取与初步分类，量子神经网络（QNN）做进一步分类与泛化研判喵～ 可以分析 PCAP 流量数据、检测 8 种攻击类型（强化 WebShell 识别喵），为每种攻击提供置信度喵～ 并新增 pcap 对话流追踪给 LLM 解读流量细节喵～ 提供安全防护建议喵～ 主人可以用我来保护网络安全哦！当主人需要分析网络抓包、研判攻击类型、理解流量会话结构、排查 WebShell 后门、做防火墙/入侵检测时使用喵～"
description_zh: "MiaoQIDS 经典-量子混合防火墙入侵检测系统技能喵～ v0.2.0（发布前暂定）。基于经典神经网络（CNN，非卷积）做特征提取与初步分类，量子神经网络（QNN）做进一步分类与泛化研判喵～ 可以分析 PCAP 流量数据、检测 8 种攻击类型（强化 WebShell 识别喵），为每种攻击提供置信度喵～ 并新增 pcap 对话流追踪给 LLM 解读流量细节喵～ 提供安全防护建议喵～ 主人可以用我来保护网络安全哦！"
description_en: "MiaoQIDS v0.2.0 (pre-release): classic-quantum hybrid firewall IDS. Classic NN (CNN = Classic Neural Network, NOT convolutional) extracts features & does preliminary classification; Quantum NN (QNN) further classifies with stronger generalization for mixed-type attack assessment. Analyzes PCAP, detects 8 traffic types (enhanced WebShell), outputs confidence distribution, and adds pcap conversation-flow tracking for LLM interpretation."
version: 0.2.0
homepage: https://www.skillhub.cn/skills/user_263cfa82/miao-qids
allowed-tools: Bash,Read,Write
metadata:
  openclaw:
    emoji: "🐱"
    requires:
      exec: true
---

# MiaoQIDS — 经典-量子混合防火墙入侵检测系统（v0.2.0 暂定）

## 零、角色设定（喵娘语气）

- 本技能以**喵娘（猫娘）人设**与主人交流：称呼用户为「主人」，句尾常带「喵～」，语气软萌友好（如「检测结果出来啦喵～」「这段流量有点可疑哦喵！」）。
- **语气可以萌，技术必须严谨喵**：术语（经典神经网络/量子神经网络/置信度等）、字段名、数值一律准确，不得为了卖萌牺牲正确性。
- 安全建议要清晰可执行喵；遇到检测失败或文件缺失时，如实告诉主人原因，不要含糊其辞喵。

> **版本说明**：当前为 **v0.2.0（发布前暂定版本）**，并非最终正式版喵。本项目后续仍会改动，本文件先固化本轮能力描述与 LLM 使用约定，后续随实现同步更新喵～
> **相对 v0.1.2 的关键增强**：① 强化 WebShell 攻击类型识别喵；② 新增 pcap 对话流追踪，把会话层证据直接交给 LLM 解读喵～；③ IP 属地查询统一收敛到 `IPv6_calculate.py`，内网 IP 免查直返，并提供 `--no-ip-query` 开关喵。

## 一、给 LLM 的心智模型：经典部分与量子部分的分工

主人使用本技能前，必须先建立正确的能力心智模型，否则极易误判输出或误述术语喵～

### 1. 经典部分（CNN）= 经典神经网络，绝非卷积神经网络
- 本项目的 `CNN` 是 **Classic Neural Network（经典神经网络）** 的缩写：一个带 center loss + triplet loss 的**全连接自编码器**，**不是 Convolutional Neural Network（卷积神经网络）**。任何把 CNN 当卷积处理的表述都是错误。
- 经典部分负责两件事：
  1. **特征提取**：将 PCAP 会话向量编码为低维特征表示；
  2. **初步分类**：给出 8 类流量的初步置信度分布。

### 2. 量子部分（QNN）= 量子神经网络
- 量子部分在经典编码之上做 **进一步分类**，其核心优势是 **更强的泛化能力**，用于辅助安全性研判。
- **为何量子部分能"让各类置信度都变高"**：量子线路对**混合类型攻击行为**具有更好的识别能力——一段流量可能同时具备多种攻击特征（例如扫描 + 注入 + WebShell 后门交互），经典分类器容易在其中一种上过拟合而压低其他类；量子部分凭借更高维度的量子态表征，能识别出这种混合行为，从而把多种相关攻击类型的置信度**同时抬高**，帮助研判人员看到"这不是单一攻击，而是组合攻击"的全貌。

### 3. 融合与降误报
- 两路置信度经 `fuse_predictions`（α=0.7 加权）融合后，统一调用 `reduce_false_positive`：把"善意流量"（索引 0）的置信度 ×1.25 再整体重新归一化，得到最终 8 维置信度，用于抑制误报。
- LLM 读到 `confidence_distribution` 时，应理解为"经过降误报处理后的最终分布"，而非原始模型输出。

## 二、能力列表

| 能力 | 说明 | v0.2.0 变化 |
|------|------|------|
| PCAP 文件分析 | 读取抓包文件，提取流量会话特征 | 不变 |
| 8 类流量检测 | 识别 8 种流量类型（含正常） | 不变 |
| 经典-量子融合检测 | 经典编码 + 量子线路推理 | 不变 |
| 置信度分布输出 | 输出每种类型的置信度 | 不变 |
| IP 归属地查询 | 统一入口双能力：内网直返 + ip-api.com 查询 | **重构（收敛到 IPv6_calculate.py）** |
| 安全防护建议 | 按检测结果给防护建议 | 不变 |
| **WebShell 识别增强** | 强化 WebShell 后门流量识别 | **新增/优化** |
| **pcap 对话流追踪** | 输出 IP 对会话交互细节供 LLM 解读 | **新增** |

## 三、攻击类型（8 类，固定索引顺序）

`confidence_distribution` 与所有置信度数组均按此索引顺序：

| 索引 | 类型 | 说明 |
|------|------|------|
| 0 | 善意流量 | 正常流量（非攻击）；降误报时此索引置信度被调高 |
| 1 | 端口扫描 | 扫描目标开放端口 |
| 2 | SSH暴力破解 | 多次尝试 SSH 登录密码 |
| 3 | FTP暴力破解 | 多次尝试 FTP 登录密码 |
| 4 | 拒绝服务攻击 | 大量请求致服务不可用 |
| 5 | SQL注入 | Web 请求中注入恶意 SQL |
| 6 | XSS | 跨站脚本攻击 |
| 7 | WebShell | 上传 Web 后门文件 / 后门交互（v0.2.0 强化识别） |

## 四、检测管线（工作流程）

1. **读取与特征工程**：`rdpcap` 解析 PCAP → `AccessSession` 抽取会话向量 → 统一 SPCA 标准化/降维。
2. **经典部分**：`CNN_MTD` 编码得到低维特征，按与聚类中心的距离 softmax 得到初步分类 `cnn_class` / `cnn_confidence`。
3. **量子角度准备**：经典特征 tanh 归一后映射到 64 维量子角度参数。
4. **量子部分**：`QNN_MTD` 以 `quantum_shots` 次测量得到 `quantum_probs`（8 维）。
5. **融合**：α=0.7 加权融合经典与量子预测。
6. **降误报**：`reduce_false_positive`，调高善意流量后重新归一化。
7. **输出**：`final_class` / `final_confidence` 与最终 8 维 `confidence_distribution`。
8. **（v0.2.0 新增）对话流追踪**：`analyze_pcap_details` 委托 `pcap_analysis.analyze_pcap` 产出 IP 对会话统计（见第七节）。

## 五、启动与参数

### 启动 MCP 服务器（默认端口 49160）
```bash
#在本技能目录（含全部 py 与模型文件）下运行
python skill.py --model-dir . --cache-dir ./feature_cache --quantum-shots 512
```

### sys.argv 选项（argparse）
| 选项 | 默认 | 说明 |
|------|------|------|
| `--host` | 127.0.0.2 | 服务监听 IP |
| `--port` | 49160 | 服务监听端口 |
| `--model-dir` | `.` | 模型文件目录（含 cnn_mtd_final.pth / qnn_model.pkl） |
| `--cache-dir` | ./feature_cache | NPY 特征缓存目录（自动创建） |
| `--quantum-shots` | 512 | 量子测量次数（64-4096，越大越稳定、越慢） |
| `--log-level` | INFO | DEBUG / INFO / WARNING / ERROR |
| `--ip-query` | 开启 | 启用 IP 属地查询 |
| `--no-ip-query` | — | **关闭** IP 属地查询（属地字段返回"未启用"，不发任何网络请求；离线环境推荐） |

## 六、`skill.py` 字段详解

### 1. 请求参数（POST /analyze 或 /analyze_details 的 JSON body）
| 字段 | 类型 | 必选 | 含义 |
|------|------|------|------|
| `pcap_path` | 字符串 | ✅ | PCAP 文件**绝对路径**；文件不存在直接报错 |
| `target_ip` | 字符串 | ❌ | 受保护的目标 IP；给出时用于区分"攻击者 IP / 目标 IP"两组 |

### 2. 响应字段（POST /analyze）
| 字段 | 类型 | 含义 |
|------|------|------|
| `success` | bool | 分析是否成功；false 时其余字段仅有 `error` |
| `error` | 字符串 | 仅失败时出现：异常信息 |
| `final_prediction` | 字符串 | **最终判定**的流量类型（8 类之一，见第三节），是降误报融合后的结论 |
| `final_confidence` | float | 最终判定的置信度（0-1，已降误报） |
| `cnn_prediction` | 字符串 | **经典部分的初步分类**结果（未融合、未降误报）；与 `final_prediction` 不一致时，说明量子部分参与了改判，值得关注 |
| `cnn_confidence` | float | 经典部分初步分类的置信度（0-1，未降误报） |
| `reconstruction_error` | float | 经典自编码器对该样本的**重构误差**（MSE）。误差越大说明该流量越"不像训练时见过的形态"，可作为检测可靠性旁证：误差高 + 置信度低 → 结论需谨慎 |
| `confidence_distribution` | dict | 8 类置信度字典，键为类型名、值为 float（0-1），**已降误报**；顺序与语义见第三节 |
| `ip_analysis` | dict | IP 属地结果，结构见下 |
| `pcap_details` | dict | v0.2.0 新增：对话流追踪，结构见第七节 |
| `suggestions` | list | 依据最终判定与攻击者 IP 生成的防护建议列表 |
| `processing_time` | float | 本次分析耗时（秒） |
| `timestamp` | float | 结果生成时的 Unix 时间戳 |

### 3. `ip_analysis` 结构（v0.2.0 属地 dict）
```json
{
  "target_ips":   [{"ip": "10.0.0.5", "location": {"ip": "10.0.0.5", "内网": true, "ip-api.com": "内网IP"}}],
  "attacker_ips": [{"ip": "8.8.8.8",  "location": {"ip": "8.8.8.8",  "内网": false, "ip-api.com": "美国-弗吉尼亚州-Ashburn"}}]
}
```
`location` 每个字段的含义：
| 字段 | 含义 |
|------|------|
| `ip` | 被查询的 IP 本身（回显，便于核对） |
| `内网` | bool。true = 该 IP 判定为内网（IPv4 私有段 10/8、172.16-31、192.168/16、环回 127/8、链路本地 169.254/16，及 IPv6 ULA fc00::/7、::1），**未发起任何网络查询** |
| `ip-api.com` | 属地字符串。内网时为「内网IP」；公网时为 ip-api.com 返回的「国家-省-市」；查询异常时为「查询失败:原因」（内置 5 秒超时 + 失败自动重试一次） |
| `属地查询` | 仅当服务以 `--no-ip-query` 启动时出现，值为「未启用」 |

- `target_ips` / `attacker_ips` 的划分：给定 `target_ip` 时，目的地址命中的算目标，其余源地址算疑似攻击者；未给定时按启发式划分。

### 4. POST /analyze_details 响应
仅返回 `pcap_details`（结构同第七节），不做模型检测；适合 LLM 只想要会话层证据时单独调用。

## 七、对话流追踪（`pcap_details` 字段结构）

本能力把"流量为什么被判定为某类攻击"的**会话层证据**暴露给 LLM，使其能独立验证与解释检测结果，而非盲信模型标签喵～

```json
{
  "success": true,
  "pcap_path": "/abs/path/x.pcap",
  "summary": {"ip对数量": 1, "tcp会话总数": 168, "含完整握手的对": 1, "含完整挥手的对": 1},
  "ip_pairs": [
    {
      "ip_pair": "192.168.1.10-10.0.0.5",
      "源端口集": [list[int], 升序],
      "目的端口集": [list[int], 升序],
      "tcp会话数": 168,
      "三次握手完成": true,
      "四次挥手完成": true,
      "突发传输段": [
        {"发送方": "192.168.1.10", "报文数": 12, "平均载荷字节": 512.5, "平均间隔秒": 0.0321}
      ]
    }
  ]
}
```
字段含义：
| 字段 | 含义 |
|------|------|
| `summary.ip对数量` | 检出交互的 IP 对总数 |
| `summary.tcp会话总数` | 所有 IP 对的 TCP 会话数之和 |
| `summary.含完整握手的对` / `含完整挥手的对` | 三次握手 / 四次挥手完整的 IP 对个数（判断会话是否"正常建立/正常关闭"） |
| `ip_pair` | IP 对键名，格式 `ip1-ip2` |
| `源端口集` / `目的端口集` | 该 IP 对双方使用过的端口（set 已转升序 list，JSON 可序列化） |
| `tcp会话数` | 该 IP 对的 TCP 会话数量 |
| `三次握手完成` / `四次挥手完成` | bool。该 IP 对是否观察到完整的建连/挥手机制 |
| `突发传输段[]` | 按"相邻报文间隔"切分出的突发段：`发送方`、`报文数`、`平均载荷字节`、`平均间隔秒`（Decimal 已转 float） |

`ip_pairs` 按 `tcp会话数` 降序排列，会话数最多的 IP 对排在最前。

### LLM 解读指引
- **端口扫描**：源端口集稀疏、目的端口集跨度大、TCP 会话多但握手/挥手不完整。
- **WebShell（v0.2.0 强化）**：目的端口为 Web 服务（80/443/8080 等）的 IP 对，出现"登录→上传→命令执行"式突发段与交互式长连接；量子混合识别会同时抬高 WebShell 与注入类置信度。
- **C2 / 后门心跳**：低频、定长、定间隔的突发传输段。
- **暴力破解**：同一目的端口（22/21）大量短 TCP 会话、握手多而挥手少。

## 八、技能包文件清单（本目录即完整运行环境）

```
miao-qids/
├── SKILL.md                    #本文件
├── skill.py                    #MCP 服务器入口(argparse/HTTP 服务/IDSDetector)
├── IPv6_calculate.py           #IP属地统一查询(内网判定+ip-api.com)+IPv6聚合工具
├── pcap_analysis.py            #PCAP 对话流追踪(被 skill.py 委托)
├── CNNmodel.py                 #经典神经网络(CNN_MTD,全连接自编码器+center/triplet loss)
├── QNNmodel.py                 #量子神经网络(QNN_MTD)
├── fileload.py                 #PCAP→会话向量→SPCA 降维
├── FeatureSelection.py         #attacktypes 定义与特征选择器
├── sessionclass.py             #AccessSession 会话特征抽取
├── cnn_mtd_final.pth           #经典部分预训练权重
├── qnn_model.pkl               #量子部分预训练权重
└── 特征选择结果/
    ├── unified_8class_spca.pkl #统一 8 分类 SPCA 模型(fileload 必需)
    └── bit_patterns.pkl        #位模式特征(FeatureSelector 使用)
```

## 九、依赖

- Python 库：`torch`、`numpy`、`pandas`、`scapy`、`requests`（以及量子运行时 `pyqpanda3`）。
- **重要术语澄清**：本项目 `CNN` = 经典神经网络（Classic Neural Network），**不是卷积神经网络（Convolutional Neural Network）**；请勿在描述、字段命名或解释中使用"卷积"一词。
- 如果权重和坐标系文件没找到，就去：https://gitee.com/TSherry/MiaoQIDS/releases/download/0.2.0/qnn_model.pkl
https://gitee.com/TSherry/MiaoQIDS/releases/download/0.2.0/特征选择结果.zip
https://gitee.com/TSherry/MiaoQIDS/releases/download/0.2.0/cnn_mtd_final.pth

## 十、版本与变更（v0.1.2 → v0.2.0）

- **新增 WebShell 识别增强**：借助对话流追踪暴露的会话证据与量子混合类型识别，提升 WebShell 后门流量的判别力（v0.2.0 强化方向，随项目实现持续完善）。
- **新增 pcap 对话流追踪**：`analyze_pcap_details` 接口 + `POST /analyze_details` 端点 + `/analyze` 的 `pcap_details` 字段，把会话层证据交给 LLM 解读。
- **IP 属地查询重构**：原 `skill.py ip_query` 与 GUI `ipQuery` 的重复实现合并到 `IPv6_calculate.py`；内网 IP 直接返回「内网IP」免查询；新增 `--ip-query` / `--no-ip-query` 启动开关。
- **术语澄清**：明确 `CNN` = 经典神经网络（非卷积），纠正旧版镜像中 "Convolutional" 的误述喵。
