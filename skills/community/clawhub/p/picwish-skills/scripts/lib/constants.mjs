export const REGION_CONFIG = {
  cn:     { baseUrl: 'https://techsz.aoscdn.com', site: 'https://picwish.cn' },
  global: { baseUrl: 'https://techhk.aoscdn.com', site: 'https://picwish.com' },
};
export const DEFAULT_REGION = 'global';

export const DEFAULT_POLL_INTERVAL_MS = 1000;
export const DEFAULT_POLL_TIMEOUT_MS  = 30_000;
export const OCR_POLL_TIMEOUT_MS      = 120_000;
export const IDPHOTO_POLL_TIMEOUT_MS  = 300_000;

export const TASK_STATE = {
  COMPLETED:  1,
  IN_QUEUE:   0,
  PREPARING:  2,
  WAITING:    3,
  PROCESSING: 4,
  TIMEOUT:       -8,
  INVALID_IMAGE: -7,
  OVERSIZE:      -5,
  DOWNLOAD_FAIL: -3,
  UPLOAD_FAIL:   -2,
  FAILED:        -1,
};
