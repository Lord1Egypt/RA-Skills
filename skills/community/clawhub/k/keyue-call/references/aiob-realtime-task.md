# AIOB 实时外呼任务（来自 `实时任务.md`）

## 接口
- URL: `https://aiob-open.baidu.com/api/v3/console/realtime/status/create`
- Method: `POST`
- Headers:
  - `Content-Type: application/json`
  - `Authorization: <accessToken>`

## 必填字段
- `robotId` (string)
- `mobile` (string)
- `secretType` (int: 1/2/3)

## 常用可选字段
- `callerNum` (string[]) 主叫号码池
- `stopDate` (string) 截止时间，格式 `yyyy-MM-dd HH:mm:ss`
- `dialogVar` (object) 对话变量；本 skill 约定优先传 `name`、`owner_name` 与 `user_intent`
- `callBackUrl` (string) 任务级回调地址
- `extJson` (string) 业务透传字段

## 响应
- `code` / `msg`
- `data.memberId`：被叫号码系统唯一标识

## 备注
- 当使用系统加密/自定义加密时，需按平台配置补齐密文字段相关参数
