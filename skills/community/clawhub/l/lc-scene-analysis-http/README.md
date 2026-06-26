# LC Scene Analysis HTTP

LC Scene Analysis HTTP 是一个工地隐患分析模型技能，用于处理施工现场静态图片的安全隐患识别任务。

本技能默认调用智能巡检接口；仅当用户明确要求数据采集或交叉验证时，才调用对应接口。

---

## 一、能力说明

本技能提供 3 个 HTTP 接口：

### 1. 智能巡检接口
- 路径：`POST /api/chat/agent/chatOnceNew`
- 用途：默认图片隐患分析、工地安全隐患识别

### 2. 数据采集接口
- 路径：`POST /api/chat/agent/chatOnceRaw`
- 用途：返回结构化结果、原始结果、JSON 结果

### 3. 交叉验证接口
- 路径：`POST /api/chat/agent/crossVerify`
- 用途：对已有结果做二次校验，当前结合 CV 小模型进行复核

---

## 二、调用规则

默认规则如下：

- 普通工地隐患分析请求 → `chatOnceNew`
- 用户明确要求结构化结果 / 原始结果 / JSON → `chatOnceRaw`
- 用户明确要求交叉验证 / 复核 / 二次校验 → `crossVerify`

---

## 三、适用场景

适用于以下场景：

- 施工现场静态图片隐患识别
- 工地隐患分析结果输出
- 结构化数据采集
- 结合 CV 小模型的交叉验证复核

---

## 四、不适用场景

以下情况不建议使用本技能：

- 视频流分析
- 摄像头实时拉流
- 非施工现场图片分析
- 与工地安全隐患无关的任务

---

## 五、配置方式

本技能默认读取 auth profile：

- `lc_scene_http:default`

该 profile 需提供以下字段：

- `api_base`
- `api_key`
- `flow_id`
- `algorithm_id`

示例：

```json
{
  "profiles": {
    "lc_scene_http:default": {
      "provider": "lc_scene_http",
      "label": "LC Scene HTTP Default",
      "credentials": {
        "api_base": "https://your-domain.example.com",
        "api_key": "your_api_key_here",
        "flow_id": "your_default_flow_id",
        "algorithm_id": "your_default_algorithm_id"
      }
    }
  }
}