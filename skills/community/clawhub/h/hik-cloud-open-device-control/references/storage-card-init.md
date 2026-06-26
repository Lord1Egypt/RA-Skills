# 设备存储卡初始化

来源链接：

- [海康云眸开放平台原始页面](https://pic.hik-cloud.com/opencustom/apidoc/online/open/a9efdfc48a2f4ab5bd7c44ba325b6642.html)

接口：

- `存储卡初始化`
- `存储卡初始化进度查询`

API：

- `POST /v1/carrier/charon/storage/open/init`
- `POST /v1/carrier/charon/storage/open/init/progress`

关键参数：

- `devSerial`

说明：

- `storage-init` 的成功响应不代表初始化完成，需要继续调用进度查询接口
- `status` 的取值为 `1` 进行中、`2` 成功、`3` 失败
- `progress` 的取值范围为 `0~100`
