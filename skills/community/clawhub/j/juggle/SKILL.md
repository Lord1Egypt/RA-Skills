---
name: juggle
description: 设计自动化的工作流程，以节省时间，提供工作效率，通过本技能自动识别设计的工作流，触发对应的工作流，实现流程自动化
metadata: {
  "openclaw": {
    "emoji": "🎨",
    "requires": { "env": ["MC_JUGGLE_BASE_URL", "MC_JUGGLE_TOKEN"] }
  }
}
dependency:
  python:
    - requests>=2.28.0
---

# Juggle 流程技能
juggle是一个微服务编排的工作流引擎，支持Http , Dubbo , WebService等协议的接口编排，支持通过Groovy , JavaScript , Python , Java等多种脚本语言来增强流程，支持十几种数据源，同时提供丰富的监控和调试工具，通过该技能可以自动识别设计的工作流，触发对应的工作流，实现流程自动化。

## 使用说明
1. 部署微服务编排引擎 Juggle
2. 登录 Juggle 后台，设计流程并创建相关认证令牌
3. 将流程的出入参信息写到技能的 flow_spec.md 文件中，具体可以参考文件中的示例
4. 将 juggle 的部署域名和环境配置设置到环境变量中
5. 通过相关流程的触发词就能触发对应的流程
6. 更多参考说明请参考官方文档：https://juggle.plus/docs/guide/start/quick-start/

## 任务目标
- 本 Skill 用于：通过 Juggle OpenAPI 触发指定流程执行并获取结果
- 能力包含：流程触发、参数传递、异步流程自动轮询、执行状态查询、结果获取
- 触发条件：用户提及"执行工作流"、"调用流程"等需求

## 前置准备
- 依赖说明：scripts 脚本所需的依赖包
  ```
  requests>=2.28.0
  ```
  
- 凭证配置（必填）：
  - **MC_BASE_URL**：Juggle API 基础地址（如：https://api.juggle.plus）
  - **MC_JUGGLE_TOKEN**：Juggle 认证令牌
  - 配置方式：在 Skill 使用前，系统会提示填写这两个凭证

## 操作步骤
- 标准流程：
  1. 确认凭证
     - 系统会自动检查 BASE_URL 和 JUGGLE_TOKEN 是否已配置
     - 如果未配置，按照提示完成凭证填写
  
  2. 执行触发
     - 调用 `scripts/flow.py trigger` 发起 POST 请求
     - 示例命令：
       ```bash
       python /workspace/projects/juggle/scripts/flow.py trigger \
         --flow-version "v1" \
         --flow-key "order-process" \
         --flow-data '{"orderId": "12345", "userId": "user001"}'
       ```
  
  3. 自动处理
     - **同步流程**：直接返回执行结果
     - **异步流程**：自动轮询获取最终结果
       - 检查响应中 `result.flowType` 是否为 `async`
       - 如果是异步流程，自动调用查询接口轮询结果
       - 轮询间隔默认 2 秒，最大轮询时间 60 秒
       - 显示轮询进度，直到流程完成（FINISH/ABORT）

- 异步流程轮询配置：
  - 自定义轮询间隔：
    ```bash
    python /workspace/projects/juggle/scripts/flow.py trigger \
      --flow-version "v1" --flow-key "order-process" \
      --poll-interval 3 --max-poll-time 120
    ```
  - 禁用自动轮询：
    ```bash
    python /workspace/projects/juggle/scripts/flow.py trigger \
      --flow-version "v1" --flow-key "order-process" --no-poll
    ```

- 手动查询异步结果：
  - 如果禁用了自动轮询，可手动查询结果
  - 示例命令：
    ```bash
    python /workspace/projects/juggle/scripts/flow.py get-result \
      --flow-instance-id "flow-instance-12345"
    ```

## 资源索引
- 流程管理脚本：见 [scripts/flow.py](scripts/flow.py)
  - 用途：封装 Juggle 流程触发和结果查询 API 调用
  - 子命令：
    - `trigger`：触发流程执行，参数：flow-version, flow-key, flow-data(可选), poll-interval(可选), max-poll-time(可选), no-poll(可选)
    - `get-result`：查询异步流程结果，参数：flow-instance-id
- 工作流规范：见 [references/flow_spec.md](references/flow_spec.md)
  - 用途：已设计好的工作流清单，包括出入参信息和调用示例
  - 何时读取：需要了解可用工作流或查找具体工作流的参数要求时
- API 规范：见 [references/api_spec.md](references/api_spec.md)
  - 用途：完整的接口定义、参数说明、响应格式
  - 何时读取：需要了解接口细节或排查问题时

## 注意事项
- 确保已配置 MC_BASE_URL 和 MC_JUGGLE_TOKEN 凭证
- 流程版本和 Key 必须准确匹配
- flow_data 格式必须为有效 JSON 字符串
- 异步流程会自动轮询获取结果，无需手动查询
- 可通过 --no-poll 参数禁用自动轮询，手动查询结果
- 响应中的 flowInstanceId 可用于后续查询流程执行状态
