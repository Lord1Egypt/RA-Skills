오픈 클로에서 모든집-아파트실거래를 한눈에! 사이트를 직접 연동해서 쓸 수 있는 패키지 입니다.
<br/>
해당 사이트는 대한민국 서울/경기등 다양한 지역과 아파트의 실거래동향 데이터와 분석을 하는 사이트입니다
<br/>
해당사이트의 모든기능을 조회할순 없으나 기본적인 지역/아파트 실거래 분석 조회가능!
<br/>
<br/>
현재 서비스지역
<br/>
-서울,경기,인천,대전,광주,대구
<br/>
<br/>
설치법
<br/>
1.openclaw 설치
<br/>
2.openclaw plugins install @brokimyeah/openclaw-eho 입력으로 다운로드
<br/>
3.openclaw.json(.openclaw폴더안에 존재)에 "plugins" 안에 "allow": ["openclaw-eho"], 추가
<br/>
(allow배열([])이 이미 있다면 기존 배열에 넣기)
<br/>
<br/>
사용법
<br/>
1.eho 사용해 원하는 지역 기간 거래형식(매매,전세,월세)조회 요청
<br/>
-tip.되도록 명확히 명령 ex)서울 서초구 서초동 00아파트 매매 정보가 궁금해 기간은 최근 3개월로
<br/>
2.필수정보는 시도와 조회기간입니다.
<br/>
3.eho 못찾을시 eho 플러그인 이용해서 조회해줘 요청 
<br/>
<br/>
기존사이트에서는 더다양한 정보를 볼 수있습니다
<br/>
https://www.everyhouse-real-payment.com/?si=%EC%84%9C%EC%9A%B8&sn=0
<br/>
계속 개선해 나가겠습니다 
<br/>
<br/>
<br/>
OpenClaw – Korean Apartment Real Transaction Data at a Glance!
This package connects directly to a Korea-based real estate analytics platform.
<br/>
This service is built on Korean real estate data and provides transaction trends and analysis for 
<br/>
apartments across major regions in South Korea, including Seoul and the surrounding metropolitan areas.
<br/>
While not all features of the original website are available, you can access essential transaction analysis by region and apartment.
<br/>
<br/>
Supported Regions
<br/>
Seoul, Gyeonggi, Incheon, Daejeon, Gwangju, Daegu
<br/>
<br/>
Installation
<br/>
Install OpenClaw
<br/>
Run openclaw plugins install @brokimyeah/openclaw-eho
<br/>
In openclaw.json (inside the .openclaw folder), add:
"allow": ["openclaw-eho"] under "plugins"
<br/>
(If the allow array already exists, simply append it)
<br/>
<br/>
Usage
<br/>
Use eho to request data by specifying region, time period, and transaction type (sale, jeonse, monthly rent)
<br/>
Tip: Be as specific as possible
Example:
“Show me sales data for XX apartment in Seocho-dong, Seocho-gu, Seoul for the last 3 months”
<br/>
Required inputs: region (at least city/province) and time period
<br/>
If the tool is not recognized, try:
“Use the eho plugin to fetch the data”
<br/>
<br/>
For full features and more detailed insights, visit:
<br/>
https://www.everyhouse-real-payment.com/?si=%EC%84%9C%EC%9A%B8&sn=0
<br/>
This service will continue to be improved over time.