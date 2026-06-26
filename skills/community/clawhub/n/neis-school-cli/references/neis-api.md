# NEIS API Notes

Official portal:
- https://open.neis.go.kr/portal/mainPage.do

Datasets used by this skill:
- `schoolInfo`
- `mealServiceDietInfo`
- `elsTimetable`
- `misTimetable`
- `hisTimetable`

Common query parameters:
- `Type=json`
- `ATPT_OFCDC_SC_CODE`
- `SD_SCHUL_CODE`

Date parameters:
- Meals: `MLSV_YMD`
- Timetable: `ALL_TI_YMD`

Important response patterns:
- Success with rows: dataset array containing `head` and `row`
- Empty result: `{"RESULT":{"CODE":"INFO-200","MESSAGE":"해당하는 데이터가 없습니다."}}`
- Success code: `INFO-000`
