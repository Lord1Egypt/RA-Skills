# 商户子账户配置SDK矩阵

## 目录

- 精确入口
- 字段与传输
- 初始化与响应

## 精确入口

2026-11-09核对当前锁定的通用Java3.0.41、PHP2.0.31和Python2.0.28源码；未声称升级或完成生产联调。类名和路由不能只按中文标题选择。

| 接口 | Java/PHP类 | Python模块 | 路由 | SDK声明字段 |
| --- | --- | --- | --- | --- |
| 子账户开通配置 | `V2MerchantSettleConfigRequest` | `v2_merchant_settle_config` | `/v2/merchant/settle/config` | `req_seq_id`, `req_date`, `huifu_id`, `upper_huifu_id`, `acct_type`, `acct_name`, `card_info` |
| 修改子账户配置 | `V2MerchantSettleModifyRequest` | `v2_merchant_settle_modify` | `/v2/merchant/settle/modify` | `req_seq_id`, `req_date`, `huifu_id`, `upper_huifu_id`, `acct_id`, `settle_config`, `card_info` |

## 字段与传输

专属类的Java完整包为 `com.huifu.bspay.sdk.opps.core.request`，PHP命名空间为 `BsPaySdk\request`，Python公开模块为 `dg_sdk.request`。Java使用对应setter和setExtendInfo，PHP使用setter和setExtendInfo，Python向生成Request属性赋值后调用post(extend_infos)。SDK声明集合只是生成类结构，不决定官网Y/N/C；其余正式字段走exact-key扩展，先拒绝覆盖已声明字段。

String(JSON Object/Array)按父路径编码；子账户card_info和settle_config不能扁平放到顶层。是否必填、空字段是否应省略由原子接口的场景决定。SDK自动放入空字段时，允许使用同一官方SDK通用入口发送校验后的精确映射，保留同一配置和签验链。

## 初始化与响应

代码任务必须补读 `shared-server-sdk-matrix.md` 的安全初始化与实际返回形状：Java在任何调用前全局关闭BasePay.debug；PHP在加载任何SDK文件前固定DEBUG=false，不使用会启用调试的Demo/Composer入口；Python MerConfig使用明确关键字，并绑定生产配置到DGClient。密钥仅从服务端安全配置读取。

通用Java已返回验签后的业务Map，不再get("data")；PHP先拒绝null/isError，再验证getRspDatas信封和data类型；Python业务数据仅在SDK验签成功后消费。未知响应保持适配点，不能以空对象冒充成功。

完整字段见 `merchant-account-complete-field-catalog.md`；分别按原子参考选择目标方向，不默认加载整份目录。
