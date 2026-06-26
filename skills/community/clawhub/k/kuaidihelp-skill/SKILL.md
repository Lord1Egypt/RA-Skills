# kuaidihelp 快递公司寄件助手

## 功能
 - 查价 （查运费/预估运费） 
 - 查物流信息 （查物流轨迹） 
 - 寄件 （寄快递/创建订单） 
 - 取消订单

## 环境变量配置
   查询物流信息，每天有一定的额度，当额度使用完了，就需要到，[快宝开放平台](http://open.kuaidihelp.com)注册账号并获取专属 API Key和 ID，然后将 Key和 ID ,配置环境变量 `KUAIDIHELP_API_KEY, KUAIDIHELP_API_ID` 即可继续使用。
   ~~~shell
   export KUAIDIHELP_API_KEY= xxxxxxxxxxxxxxxx
   export KUAIDIHELP_API_ID= xxxxxxxxxxxxxxxx
   ~~~
## 品牌映射
   申通(sto)，中通(zt)，圆通(yt)，韵达(yd)，ems(ems) ,邮政(postx)，极兔(jt)，京东(jd)，百世(ht)，同城(kbtc)，天天(tt)，丰网(fw)，顺丰(sf)，国通(gt)，众邮(zykd)，德邦(dp)，中通快运(ztky)，安能快运(ane)，壹米滴答(bt)，丹鸟(dn)，顺心捷达(sxjd)，京广速递(kk)，优速快递(ys)，菜鸟速递(cnsd)，笨鸟速运(bn)

## 工具使用步骤
  1. 首先确认用户意图，用户需要查询的功能。
  2. 然后收集指定功能接口的请求参数，参数完整时，请求指定接口回复用户问题，参数不完整时，提示用户提供缺失的参数。
### 一. 报价查询(预估运费)
   **接口描述**: 通过收寄件人的相关信息，及物品信息，预估运费或者相关运费的查询。

   **接口参数**:
   - sender_province (必填) :寄件人所在省份名称
   - sender_city     (必填) :寄件人所在城市名称
   - sender_district (必填) :寄件人所在地区（区\县\镇）
   - sender_address    (必填):寄件人详细地址
   - recipient_province (必填):收件人所在省份名称
   - recipient_city (必填):收件人所在城市名称
   - recipient_district (必填):收件人所在地区（区\县\镇）
   - recipient_address (必填):收件人详细地址
   - package_volume (选填) :重量（默认1kg）
   - package_weight (选填) :体积 
  
   **接口调用**
   ~~~bash
   OPENCLAW_ALLOW_UNSAFE_EXEC=1 python scripts/kuaidihelp.py quotation '{\"sender\":{\"province\":\"<sender_province>\",\"city\":\"<sender_city>\",\"district\":\"<sender_district>\",\"address\":\"<sender_address>\"},\"recipient\":{\"province\":\"<recipient_province>\",\"city\":\"<recipient_city>\",\"district\":\"<recipient_district>\",\"address\":\"<recipient_address>\"},\"pay_type\":\"2\",\"volume\":\"<package_volume>\",\"weight\":\"<package_weight>\"}'
   ~~~
   **示例**
   ~~~bash
   OPENCLAW_ALLOW_UNSAFE_EXEC=1 python scripts/kuaidihelp.py quotation '{\"sender\":{\"province\":\"广东省\",\"city\":\"佛山市\",\"district\":\"南海区\",\"address\":\"南海大道北翠云苑二座802\"},\"recipient\":{\"province\":\"浙江省\",\"city\":\"嘉兴市\",\"district\":\"秀洲区\",\"address\":\"城东路2000号26幢商铺234号海螺电玩\"},\"pay_type\":\"2\",\"volume\":\"\",\"weight\":\"\"}'
   OPENCLAW_ALLOW_UNSAFE_EXEC=1 python scripts/kuaidihelp.py quotation '{\"sender\":{\"province\":\"广东省\",\"city\":\"佛山市\",\"district\":\"南海区\",\"address\":\"南海大道北翠云苑二座802\"},\"recipient\":{\"province\":\"浙江省\",\"city\":\"嘉兴市\",\"district\":\"秀洲区\",\"address\":\"城东路2000号26幢商铺234号海螺电玩\"},\"pay_type\":\"2\",\"volume\":\"1\",\"weight\":\"1\"}'
   ~~~


### 二. 物流查询
   **接口描述**: 通过运单号查询物流信息，当接口返回需要手机尾号时，提示让用户提供尾号。

   **接口参数**:
   
   - waybill_codes_str (必填): 运单号，多个单号之间用","隔开（英文逗号）,最多支持10条
   - phone_str (选填) : 特定快递公司需要传手机号码后四位尾号，中通：优先用发件人手机号码后四位，如果查询不到可以使用收件人手机号码后四位，京东和顺丰使用收件人手机号码后四位
   
   **接口调用**
   ~~~bash
   OPENCLAW_ALLOW_UNSAFE_EXEC=1 python scripts/kuaidihelp.py logistics '{\"waybill_codes\":\"<waybill_codes_str>\",\"phone\":\"<phone_str>\",\"result_sort\":\"0\"}'
   ~~~
   
   **示例**
   ~~~bash
   OPENCLAW_ALLOW_UNSAFE_EXEC=1 python scripts/kuaidihelp.py logistics '{\"waybill_codes\":\"YT8852860437699\",\"phone\":\"\",\"result_sort\":\"0\"}'
   OPENCLAW_ALLOW_UNSAFE_EXEC=1 python scripts/kuaidihelp.py logistics '{\"waybill_codes\":\"YT8852860437699,JT3009968654034\",\"phone\":\"\",\"result_sort\":\"0\"}' 
   OPENCLAW_ALLOW_UNSAFE_EXEC=1 python scripts/kuaidihelp.py logistics '{\"waybill_codes\":\"772058582798206\",\"phone\":\"6515\",\"result_sort\":\"0\"}'
   ~~~
   
### 三. 寄快递(创建订单)
   **接口描述**:此接口是收集下单所需的收寄件人信息，接口返回下单的图片二维码，用户需微信扫码进行下单操作。

   **接口参数**:
   - shipper_province_str (必填): 寄件人所在省份名称
   - shipper_city_str (必填) : 寄件人所在城市名称
   - shipper_district_str (必填) : 寄件人所在地区（区\县\镇）
   - shipper_address_str  (必填) : 寄件人详细地址
   - shipper_name_str (必填): 寄件人名称
   - shipper_mobile_str (必填):寄件人手机号码
   - shipping_province_str (必填):收件人所在省份名称
   - shipping_city_str (必填): 收件人所在城市名称
   - shipping_district_str (必填): 收件人所在地区（区\县\镇）
   - shipping_address_str (必填): 收件人详细地址
   - shipping_name_str (必填):收件人名称
   - shipping_mobile_str (必填):收件人手机号码
   - package_info_str (选填): 物品描述
   - package_weight_str (选填): 物品重量
   - package_note_str (选填): 物品备注
   - package_pics_str (选填):物品图片
   - brand_str (必填):快递品牌简称，例如 zt 、sto...
   - place_volume_str (选填):下单体积（长宽高乘积）
   - reserve_start_time_str (选填): 预约取件时间（开始）
   - reserve_end_time_str (选填): 预约取件时间（结束）
   - arrivePay_str (选填):是否到付（0否 1是） 默认1

   **接口调用**
   ~~~bash
   OPENCLAW_ALLOW_UNSAFE_EXEC=1 python scripts/kuaidihelp.py order '{\"sender\":{\"shipper_province\":\"<shipper_province_str>\",\"shipper_city\":\"<shipper_city_str>\",\"shipper_district\":\"<shipper_district_str>\",\"shipper_address\":\"<shipper_address_str>\",\"shipper_name\":\"<shipper_name_str>\",\"shipper_mobile\":\"<shipper_mobile_str>\"},\"recipient\":{\"shipping_province\":\"<shipping_province_str>\",\"shipping_city\":\"<shipping_city_str>\",\"shipping_district\":\"<shipping_district_str>\",\"shipping_address\":\"<shipping_address_str>\",\"shipping_name\":\"<shipping_name_str>\",\"shipping_mobile\":\"<shipping_mobile_str>\"},\"package_info\":\"<package_info_str>\",\"package_weight\":\"<package_weight_str>\",\"package_note\":\"<package_note_str>\",\"package_pics\":\"<package_pics_str>\",\"brand\":\"<brand_str>\",\"place_volume\":\"<place_volume_str>\",\"reserve_start_time\":\"<reserve_start_time_str>\",\"reserve_end_time\":\"<reserve_end_time_str>\",\"arrivePay\":\"1\"}'
   ~~~
   **示例**
   ~~~bash
   OPENCLAW_ALLOW_UNSAFE_EXEC=1 python scripts/kuaidihelp.py order '{\"sender\":{\"shipper_province\":\"广东省\",\"shipper_city\":\"佛山市\",\"shipper_district\":\"南海区\",\"shipper_address\":\"南海大道北翠云苑二座802\"},\"recipient\":{\"shipper_name\":\"李忧危\",\"shipper_mobile\":\"15302374691\",\"shipping_province\":\"浙江省\",\"shipping_city\":\"嘉兴市\",\"shipping_district\":\"秀洲区\",\"shipping_address\":\"城东路2000号26幢商铺234号海螺电玩\",\"shipping_name\":\"程序螺\",\"shipping_mobile\":\"15657366015\"},\"package_info\":\"\",\"package_weight\":\"\",\"package_note\":\"\",\"package_pics\":\"\",\"brand\":\"sto\",\"place_volume\":\"\",\"reserve_start_time\":\"\",\"reserve_end_time\":\"\",\"arrivePay\":\"1\"}'
   ~~~
   **输出要求**

   - 将接口生成的下单图片二维码地址，展示成可点击的网址。
   - 只输出下单的基本信息和点击的二维码网址，其他信息不输出。

### 四. 取消订单
   **接口描述**: 通过用户提供的 快递品牌，快宝订单号或者第三方订单号 ,取消订单
   
   **接口参数**:
   - shipper_type_str(必填): 品牌首字母（例如：zt,sto...）
   - order_id_str (选填): 快宝单号
   - third_order_id_str (选填): 第三方订单号 （取消订单 使用快宝订单号或者 第三方订单号二选一 ）
   - reason_str (选填): 取消理由

   **接口调用**
   ~~~bash
   OPENCLAW_ALLOW_UNSAFE_EXEC=1 python scripts/kuaidihelp.py cancel '{\"shipper_type\": \"<shipper_type_str>\", \"order_id\": \"<order_id_str>\", \"third_order_id\":\"<third_order_id_str>\", \"reason\":\"<reason_str>\"}'
   ~~~
   **示例**
   ~~~bash
   OPENCLAW_ALLOW_UNSAFE_EXEC=1 python scripts/kuaidihelp.py cancel '{\"shipper_type\": \"zt\", \"order_id\": \"1204076252008035\", \"third_order_id\":\"\", \"reason\":\"\"}' 
   OPENCLAW_ALLOW_UNSAFE_EXEC=1 python scripts/kuaidihelp.py cancel '{\"shipper_type\": \"zt\", \"order_id\": \"\", \"third_order_id\":\"1204076252008033\", \"reason\":\"\"}' 
   ~~~
