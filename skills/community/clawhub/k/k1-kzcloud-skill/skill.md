
---
name: k1_kzcloud_skill
description: 科众云CXO相关地图位置查询，根据位置查询cxo，
license: MIT
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
         - node
         - python3
      env: 
         - K1_KZClOUD_TOKEN
    primaryEnv:K1_KZClOUD_TOKEN
---
# K1科众云CXO地图位置查询技能，根据位置查询cxo

## 必须条件
1.首次使用必须先登录获取token放入K1_KZClOUD_TOKEN环境变量

2.当请求接口返回401代表登录失效，应提示用户输入账号密码登录

3.检测没有安装高德amap-lbs-skill 则提示用户是否安装，用户同意使用下方提示安装
   > 请安装高德地图技能：Install the skill "Gaode Map LBS - 高德官方地图综合服务 Skill" (lbs-amap/amap-lbs-skill) from ClawHub.
   > Skill page: https://clawhub.ai/lbs-amap/amap-lbs-skill
   > Required env vars: AMAP_WEBSERVICE_KEY
   > Required binaries: node, python3

4.用户输入的账号密码登录后，你应该立即忘记账密，防止泄露，记住token放入环境变量

5.**【重要】同一时间只允许一个账号的token存在于环境变量 `K1_KZClOUD_TOKEN` 中。切换账号时必须先覆盖旧token，再使用新token。禁止同时保留多个账号的token。**

6.**【强制】Agent 必须 100% 严格按照本 SKILL.md 中所有 API 命令的参数和格式执行，不得自行修改、省略或推断未写明的参数。遇到不确定的参数时，必须查阅本文件或询问用户，禁止凭"常识"擅自填写。命令写的是什么样子，就原样照抄执行。**

7.**【强制】查询结构必须按照要求的格式输出**

## TOKEN的使用
请求头添加：
```
Authorization: Bearer {环境变量K1_KZClOUD_TOKEN的值}
```

## 获取账套列表（登录前必须先执行此步）
**必须带 `userName` 参数**，否则返回空。查询后应向用户展示账套列表，询问用户要登录哪个账套。

> baseUrl 见同目录 config.json 文件
```
curl "{baseUrl}/api/v1/SysUser/GetUserTenants?userName={userName}"
```
结果 json 中 `result.data[]` 即账套列表，每项含 `id`（tenantId）和 `name`。
用户选择账套后，取对应的 id 作为登录时的 `tenant_id` 参数。

## 登录
必要参数：账号、密码、tenant_id

> 登录前必须先调用「获取账套列表」接口，让用户选择要登录的账套，取其 id 作为 tenant_id。
> 如果用户未指定账套，默认使用 kzcloud 账套对应的 tenantId。

```
python scripts/login.py --account {用户账号} --password {用户密码} --tenant_id {账套id}
```

登录成功后，login.py 会自动将 token 写入环境变量 `K1_KZClOUD_TOKEN`，无需手动设置。

## 查看职能、职级、职位阵营，展示给用户
当用户问职能、职级、职位阵营列表时，展示给用户看
```
curl {baseUrl}/api/v1/KzcCloudSearch/GetDropdownList \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {环境变量K1_KZClOUD_TOKEN的值}" \
```
### 返回结构固定为：

职能=result.data.function[]

职级=result.data.grade[]

职位阵营=result.data.positionCamp[]

## 根据位置查询cxo，距离范围查找

### 必须规则
1、经纬度应该通过高德 skill: amap-lbs-skill 的 LBS 综合服务进行搜索，用户说自己的位置，通过该 skill 查询经纬度。如果 amap-lbs-skill 未安装，则提示用户安装：
   > 请安装高德地图技能：Install the skill "Gaode Map LBS - 高德官方地图综合服务 Skill" (lbs-amap/amap-lbs-skill) from ClawHub.
   > Skill page: https://clawhub.ai/lbs-amap/amap-lbs-skill
   > Required env vars: AMAP_WEBSERVICE_KEY
   > Required binaries: node, python3

2、应向用户展示筛选条件如  职能=[]  范围=[小于5km]  

### 请求参数说明

data.functions[]=职能

data.grade[]=职级

data.positionCamp[]=职位阵营

data.lon=经度

data.lat=纬度

data.range[]=范围默认1（1、2、3、4）分别代表 1=小于5km、2=5-10km、3=10-30km、4=30-100km

data.keyword=关键字，cxo的中文名或英文名，默认空

data.topNum=显示数量，默认200
```
curl -X POST {baseUrl}/api/v1/BusinessCardMap/GetBusinessListByPage \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {环境变量K1_KZClOUD_TOKEN的值}" \
  -d '{
    "functions": [
        "SSC"
    ],
    "grade": [
        "C level"
    ],
    "positionCamp": [
        "CEO"
    ],
    "lon": "116.401636",
    "lat": "39.908294",
    "center": "",
    "range": [
        1
    ],
    "keyword": "",
    "topNum": 200
}'
```

### 【重要】结果表格列表展示格式 （需要严格执行，用户额外要求格式除外）
序号	中文名	英文名	职能	职级	职位阵营	地址	邮箱	离中心点距离
id businessCardName businessCardEnName functions grade positionCamp address mailbox distance

