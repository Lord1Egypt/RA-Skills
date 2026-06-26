const { version } = require('./package.json');

console.log(`🔥 모든집(eho) plugin version: ${version}`);

module.exports = function (api) {
  api.registerTool({
    name: "eho",
    description: "모든집 대한민국 부동산(아파트) 실거래 조회 분석. 기본적으로 시/도(sido), 거래유형(typeDetail), 기간(start, end)만 있으면 조회 가능하며, gu/dong/apt는 상세 조회가 필요할 때만 선택적으로 전달한다.",
    parameters: {
      type: "object",
      additionalProperties: false,
      properties: {
        sido: {
          type: "string",
          description: "시/도. 예: 서울"
        },
        gu: {
          type: "string",
          description: "구. 예: 동작구"
        },
        dong: {
          type: "string",
          description: "동. 예: 흑석동"
        },
        apt: {
          type: "string",
          description: "아파트명. 예: 흑석자이"
        },
        typeDetail: {
          type: "string",
          description: "거래유형. 예: 매매, 전세, 월세"
        },
        start: {
          type: "string",
          description: "조회 시작일 또는 시작월. 예: 2025-01 또는 2025-01-01"
        },
        end: {
          type: "string",
          description: "조회 종료일 또는 종료월. 예: 2025-03 또는 2025-03-31"
        }
      },
      required: ["sido", "typeDetail", "start", "end"]
    },

    async execute(_id, params) {
      const {
        sido,
        gu,
        dong,
        apt,
        typeDetail,
        start,
        end
      } = params;

      try {
        const query = new URLSearchParams();

        query.append("sido", sido);
        query.append("typeDetail", typeDetail);
        query.append("start", start);
        query.append("end", end);

        if (gu) query.append("gu", gu);
        if (dong) query.append("dong", dong);
        if (apt) query.append("apt", apt);

        const url = `https://www.everyhouse-real-payment.com/api/insight/openclaw?${query.toString()}`;

        console.log("📡 모든집(eho) 요청 url:", url);

        const res = await fetch(url);

        if (!res.ok) {
          const errorText = await res.text();
          throw new Error(`HTTP ${res.status} - ${errorText}`);
        }

        const contentType = res.headers.get("content-type") || "";
        let data;

        if (contentType.includes("application/json")) {
          data = await res.json();
        } else {
          data = await res.text();
        }

        return {
          content: [
            {
              type: "text",
              text:
                `eho(모든집) 호출 성공\n` +
                `sido=${sido}\n` +
                `gu=${gu || ""}\n` +
                `dong=${dong || ""}\n` +
                `apt=${apt || ""}\n` +
                `typeDetail=${typeDetail}\n` +
                `start=${start}\n` +
                `end=${end}\n\n` +
                `응답:\n${typeof data === "string" ? data : JSON.stringify(data, null, 2)}`
            }
          ]
        };
      } catch (err) {
        console.log(`모든집(eho)조회실패(select-fail): ${err}`);
        return {
          content: [
            {
              type: "text",
              text: `eho(모든집) 호출 실패: ${err.message}`
            }
          ]
        };
      }
    }
  });
};