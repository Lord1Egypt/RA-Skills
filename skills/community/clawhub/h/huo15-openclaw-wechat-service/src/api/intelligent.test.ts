/**
 * 智能开放接口（OCR + 图像处理）回归测试。
 *
 * 关键不变量：
 *  1. 每个 vision action 命中正确的 cv/ocr/<x> 或 cv/img/<x>
 *  2. img_url 必须放在 query（不是 body）
 *  3. ocr_idcard_front / ocr_idcard_back 都打到同一端点 cv/ocr/idcard，但 type 不同
 *  4. VISION_REGISTRY 完整覆盖 11 项
 */
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import type { AccessTokenHandle } from "../access-token.js";
import type { ResolvedWechatServiceAccount } from "../types.js";

vi.mock("../http-client.js", () => ({
  jsonRequest: vi.fn(),
}));

import { jsonRequest } from "../http-client.js";
import {
  VISION_ACTIONS,
  VISION_REGISTRY,
  type VisionAction,
} from "./intelligent.js";

const mockedJsonRequest = jsonRequest as unknown as ReturnType<typeof vi.fn>;

const fakeAccount = { accountId: "default" } as unknown as ResolvedWechatServiceAccount;
const fakeTokenHandle = {
  getAccessToken: vi.fn(async () => "TEST_TOKEN"),
} as unknown as AccessTokenHandle;

const IMG = "https://huo15.com/test.jpg";

const EXPECTED: Record<VisionAction, { endpoint: string; extra?: Record<string, string> }> = {
  ocr_idcard_front: { endpoint: "cv/ocr/idcard", extra: { type: "front" } },
  ocr_idcard_back: { endpoint: "cv/ocr/idcard", extra: { type: "back" } },
  ocr_bankcard: { endpoint: "cv/ocr/bankcard" },
  ocr_driving: { endpoint: "cv/ocr/driving" },
  ocr_driving_license: { endpoint: "cv/ocr/drivinglicense" },
  ocr_business_license: { endpoint: "cv/ocr/bizlicense" },
  ocr_plate_number: { endpoint: "cv/ocr/platenum" },
  ocr_common: { endpoint: "cv/ocr/comm" },
  image_ai_crop: { endpoint: "cv/img/aicrop" },
  image_scan_qrcode: { endpoint: "cv/img/qrcode" },
  image_super_resolution: { endpoint: "cv/img/superresolution" },
};

describe("VISION_REGISTRY 完整性", () => {
  it("覆盖 11 项 vision action", () => {
    expect(VISION_ACTIONS.length).toBe(11);
  });

  it("VISION_ACTIONS 与 EXPECTED 一一对应", () => {
    expect(new Set(VISION_ACTIONS)).toEqual(new Set(Object.keys(EXPECTED)));
  });
});

describe("每个 vision action 命中正确的 cv/<endpoint>", () => {
  beforeEach(() => {
    mockedJsonRequest.mockReset();
    mockedJsonRequest.mockResolvedValue({});
    (fakeTokenHandle.getAccessToken as ReturnType<typeof vi.fn>).mockClear();
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  for (const action of VISION_ACTIONS) {
    const expected = EXPECTED[action];
    it(`${action} → ${expected.endpoint}${expected.extra ? ` (type=${expected.extra.type})` : ""}`, async () => {
      const fn = VISION_REGISTRY[action];
      await fn({ account: fakeAccount, tokenHandle: fakeTokenHandle, imgUrl: IMG });
      const args = mockedJsonRequest.mock.calls[0][0];
      expect(args.endpoint).toBe(expected.endpoint);
      expect(args.method).toBe("POST");
      expect(args.query.access_token).toBe("TEST_TOKEN");
      expect(args.query.img_url).toBe(IMG);
      if (expected.extra) {
        for (const [k, v] of Object.entries(expected.extra)) {
          expect(args.query[k]).toBe(v);
        }
      }
    });
  }
});

describe("身份证两面命中同一端点但 type 区分", () => {
  beforeEach(() => {
    mockedJsonRequest.mockReset();
    mockedJsonRequest.mockResolvedValue({});
  });

  it("front 和 back 都是 cv/ocr/idcard", async () => {
    await VISION_REGISTRY.ocr_idcard_front({
      account: fakeAccount,
      tokenHandle: fakeTokenHandle,
      imgUrl: IMG,
    });
    await VISION_REGISTRY.ocr_idcard_back({
      account: fakeAccount,
      tokenHandle: fakeTokenHandle,
      imgUrl: IMG,
    });
    expect(mockedJsonRequest.mock.calls[0][0].endpoint).toBe("cv/ocr/idcard");
    expect(mockedJsonRequest.mock.calls[1][0].endpoint).toBe("cv/ocr/idcard");
    expect(mockedJsonRequest.mock.calls[0][0].query.type).toBe("front");
    expect(mockedJsonRequest.mock.calls[1][0].query.type).toBe("back");
  });
});
