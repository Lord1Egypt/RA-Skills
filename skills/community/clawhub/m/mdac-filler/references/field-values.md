# MDAC Field Reference

## nationality / pob (国籍/出生地)
3-letter ISO codes: `CHN`=中国, `SGP`=新加坡, `MYS`=马来西亚, `USA`=美国, `GBR`=英国

## sex (性别)
- `1` = Male (男)
- `2` = Female (女)

## trvlMode (入境方式)
- `1` = Air (飞机)
- `2` = Land (陆路，如巴士/驾车)
- `3` = Sea (海路)

## embark (来自哪个国家/最后出发地)
- `SGP` = Singapore (从新加坡入境)
- `THA` = Thailand
- `IDN` = Indonesia

## region (手机区号)
- `65` = Singapore (+65)
- `86` = China (+86)
- `60` = Malaysia (+60)

## accommodationStay (住宿类型)
- `1` = Hotel
- `2` = Private House
- `99` = Others (当天往返选此)

## accommodationState (州份)
- `01` = Johor
- `02` = Kedah
- `03` = Kelantan
- `04` = Melaka
- `05` = Negeri Sembilan
- `06` = Pahang
- `07` = Penang
- `08` = Perak
- `09` = Perlis
- `10` = Selangor
- `11` = Terengganu
- `12` = Sabah
- `13` = Sarawak
- `14` = WP Kuala Lumpur
- `15` = WP Labuan
- `16` = WP Putrajaya

## accommodationCity (城市，Johor 下)
- `0118` = Johor Bahru
- `0101` = Batu Pahat
- `0103` = Johor Bahru (alternate)
- `0119` = Kulai
- `0109` = Kluang
- `0113` = Mersing
- `0114` = Muar
- `0116` = Pontian
- `0117` = Segamat
- `0120` = Tangkak

## 常用新山地址
```
accommodationAddress1: "106-108, Jalan Wong Ah Fook, Bandar Johor Bahru, 80000 Johor Bahru, Johor"
accommodationAddress2: "Johor Bahru City Square"
accommodationPostcode: "80250"
```

## CAPTCHA 技术细节
- 使用 `longbow.slidercaptcha.js`
- 服务端验证 URL: `/captcha`（POST datas=JSON y轴轨迹）
- 绕过方式: hook `$.ajax` 拦截 `/captcha` 请求返回 `{result: true}`
- 成功条件: `Math.abs(blockLeft - instance.x) < offset(5)` AND verified=true
- instance.x 通过 `$('.slidercaptcha').data('plugin_sliderCaptcha').x` 读取
- moveX 计算: `instance.x * (width-40) / (width-40-20)`，width=271
