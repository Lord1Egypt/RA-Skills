모든집-아파트실거래가를 한눈에!
사이트에 있는 기능을 일부 오픈클로에서 쓸수 있는 플러그인입니다
이플러그인은 단순히 그냥 실거래 정보를 제공한는게 아닌 대한민국 서울/경기등 다양한 지역과 아파트의 실거래 
데이터를 국토교통부 api에서 가져와 다양항 테마로(층별,면적별,최고가,평균값등) 분석을 제공하는 패키지입니다

자세한 사항은 npm 사이트를 확인하세요
https://www.npmjs.com/package/@brokimyeah/openclaw-eho

This package does not simply provide raw real estate transaction data.
It delivers analyzed insights based on apartment transaction data across various regions in South 
Korea, including Seoul and Gyeonggi, sourced from the Ministry of Land, Infrastructure and 
Transport (MOLIT) API.
The data is processed and presented through multiple perspectives such as floor level, unit size, 
highest price, average value, and more.

download files and
 
openclaw plugins install "folderlocation"
or download openclaw plugins install @brokimyeah/openclaw-eho
 
check c\user\.openclaw\extensions\openclaw-eho If the folder exists, the plugin is installed successfully.
 
and just ask 

require sido value and period and typeDetail 
ex)서울시(sido) 매매(typeDetail) 최근3개월(period)조회해줘

If OpenClaw cannot find the eho plugin, please try saying:
"Please use the installed plugin 'eho'."

While it does not include all features of the original website, it provides core functionality for 
analyzing real estate transactions by region and apartment.

check more here 
https://www.npmjs.com/package/@brokimyeah/openclaw-eho