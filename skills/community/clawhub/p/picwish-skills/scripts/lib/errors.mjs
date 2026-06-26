import { REGION_CONFIG, DEFAULT_REGION } from './constants.mjs';

function getSiteUrl() {
  const region = process.env.PICWISH_REGION?.trim()?.toLowerCase() || DEFAULT_REGION;
  return REGION_CONFIG[region]?.site || REGION_CONFIG[DEFAULT_REGION].site;
}

const HTTP_ERRORS = {
  401: {
    error_type: 'AUTH_FAILED',
    user_hint: 'Invalid API key or service not activated.',
    next_action: 'Please check PICWISH_API_KEY.',
  },
  400: {
    error_type: 'PARAM_ERROR',
    user_hint: 'Invalid request parameters.',
    next_action: 'Please check required fields and value ranges.',
  },
  404: {
    error_type: 'NOT_FOUND',
    user_hint: 'Endpoint or task_id does not exist.',
    next_action: 'Please verify the API path.',
  },
  413: {
    error_type: 'FILE_TOO_LARGE',
    user_hint: 'File exceeds size limit.',
    next_action: 'Please refer to the API docs for maximum file size.',
  },
  429: {
    error_type: 'RATE_LIMITED',
    user_hint: 'QPS limit exceeded (default: 2).',
    next_action: 'Please reduce request frequency.',
  },
  500: {
    error_type: 'SERVER_ERROR',
    user_hint: 'PicWish server error.',
    next_action: 'Please retry later or contact support.',
  },
};

const TASK_STATE_ERRORS = {
  '-8': {
    error_type: 'TASK_TIMEOUT',
    user_hint: 'Processing timed out (>30s).',
    next_action: 'Please try a smaller or simpler image.',
  },
  '-7': {
    error_type: 'INVALID_IMAGE',
    user_hint: 'Image is corrupted or format not supported.',
    next_action: 'Please check that the image file is valid.',
  },
  '-5': {
    error_type: 'IMAGE_OVERSIZE',
    user_hint: 'Image exceeds dimension limit.',
    next_action: 'Please resize the image and retry.',
  },
  '-3': {
    error_type: 'DOWNLOAD_FAILED',
    user_hint: 'Server failed to download the image URL.',
    next_action: 'Please verify the URL is accessible.',
  },
  '-2': {
    error_type: 'UPLOAD_FAILED',
    user_hint: 'Result upload failed.',
    next_action: 'Please retry.',
  },
  '-1': {
    error_type: 'TASK_FAILED',
    user_hint: 'Processing failed.',
    next_action: 'Please retry or use a different image.',
  },
};

function getApiKeyUrl() {
  return `${getSiteUrl()}/my-account?subRoute=api-key`;
}

function getStatusPageUrl() {
  return `${getSiteUrl()}/states`;
}

export function buildHttpError(statusCode, message) {
  const template = HTTP_ERRORS[statusCode] || {
    error_type: 'UNKNOWN_HTTP_ERROR',
    user_hint: `HTTP ${statusCode} error.`,
    next_action: 'Please retry later.',
  };

  const isAuth = statusCode === 401;
  const actionUrl = isAuth ? getApiKeyUrl() : getStatusPageUrl();
  const actionLabel = isAuth ? 'Get API Key' : 'View Error Details';

  return {
    ok: false,
    error_type: template.error_type,
    error_code: statusCode,
    user_hint: template.user_hint,
    next_action: template.next_action,
    action_url: actionUrl,
    action_label: actionLabel,
    action_link: `[${actionLabel}](${actionUrl})`,
    ...(message ? { raw_message: message } : {}),
  };
}

export function buildTaskStateError(state) {
  const actionUrl = getStatusPageUrl();
  const actionLabel = 'View Error Details';
  const template = TASK_STATE_ERRORS[String(state)] || {
    error_type: 'UNKNOWN_TASK_ERROR',
    user_hint: `Unexpected task state (state=${state}).`,
    next_action: 'Please retry.',
  };

  return {
    ok: false,
    error_type: template.error_type,
    error_code: state,
    user_hint: template.user_hint,
    next_action: template.next_action,
    action_url: actionUrl,
    action_label: actionLabel,
    action_link: `[${actionLabel}](${actionUrl})`,
  };
}
