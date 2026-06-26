import { CliError, ExitCode, getGmapsApiKey } from "./config.ts";
import { requestWithRetry, type HttpRequest } from "./http.ts";
import type { CommandDef, HttpResult } from "./types.ts";

export interface EngineDependencies {
  requestFn?: (request: HttpRequest) => Promise<HttpResult>;
  apiKey?: string;
  timeoutMs?: number;
  retries?: number;
}

export async function executeCommandDef(
  command: CommandDef,
  flags: Record<string, string>,
  dependencies: EngineDependencies = {},
): Promise<unknown> {
  const apiKey = dependencies.apiKey ?? getGmapsApiKey();
  const requestFn = dependencies.requestFn ?? requestWithRetry;
  const { params, body } = command.buildRequest(flags);

  const url = command.buildUrl ? command.buildUrl(flags) : command.url;

  const headers: Record<string, string> = {};
  let requestParams: Record<string, string> | undefined = params;

  if (command.auth === "query") {
    requestParams = { ...params, key: apiKey };
  } else {
    headers["X-Goog-Api-Key"] = apiKey;
  }

  if (command.fieldMask) {
    headers["X-Goog-FieldMask"] = command.fieldMask;
  }

  const httpRequest: HttpRequest = {
    method: command.method,
    url,
    params: requestParams,
    headers,
    body,
    timeoutMs: dependencies.timeoutMs,
    retries: dependencies.retries,
  };

  const { status, payload } = await requestFn(httpRequest);

  if (!command.checkSuccess(status, payload)) {
    throw new CliError(
      `Google Maps API error for ${command.name}: ${command.getErrorMessage(payload)}`,
      ExitCode.API_BUSINESS,
      { rawResponse: payload },
    );
  }

  return payload;
}
