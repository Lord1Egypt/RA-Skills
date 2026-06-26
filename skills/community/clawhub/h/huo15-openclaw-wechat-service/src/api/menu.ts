/**
 * 自定义菜单 API
 *
 * https://developers.weixin.qq.com/doc/offiaccount/Custom_Menus/Creating_Custom-Defined_Menu.html
 *
 * 支持基础菜单 + 个性化菜单（conditional menu）。
 */

import { jsonRequest } from "../http-client.js";
import type { AccessTokenHandle } from "../access-token.js";
import type { ResolvedWechatServiceAccount } from "../types.js";

export type WechatMenuButton =
  | {
      type: "click";
      name: string;
      key: string;
      sub_button?: WechatMenuButton[];
    }
  | {
      type: "view";
      name: string;
      url: string;
      sub_button?: WechatMenuButton[];
    }
  | {
      type: "miniprogram";
      name: string;
      url?: string;
      appid: string;
      pagepath: string;
      sub_button?: WechatMenuButton[];
    }
  | {
      type:
        | "scancode_push"
        | "scancode_waitmsg"
        | "pic_sysphoto"
        | "pic_photo_or_album"
        | "pic_weixin"
        | "location_select";
      name: string;
      key: string;
      sub_button?: WechatMenuButton[];
    }
  | {
      type: "media_id" | "view_limited";
      name: string;
      media_id: string;
      sub_button?: WechatMenuButton[];
    }
  | {
      type: "parent";
      name: string;
      sub_button: WechatMenuButton[];
    };

export async function createCustomMenu(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  buttons: WechatMenuButton[];
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/menu/create",
    query: { access_token: accessToken },
    body: { button: params.buttons },
    network: params.account.network,
  });
}

export async function getCustomMenu(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
}): Promise<Record<string, unknown>> {
  const accessToken = await params.tokenHandle.getAccessToken();
  return jsonRequest<Record<string, unknown>>({
    method: "GET",
    endpoint: "cgi-bin/get_current_selfmenu_info",
    query: { access_token: accessToken },
    network: params.account.network,
  });
}

export async function deleteCustomMenu(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "GET",
    endpoint: "cgi-bin/menu/delete",
    query: { access_token: accessToken },
    network: params.account.network,
  });
}

export type ConditionalMatchRule = {
  tag_id?: string;
  sex?: string;
  client_platform_type?: string;
  country?: string;
  province?: string;
  city?: string;
  language?: string;
};

export async function createConditionalMenu(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  buttons: WechatMenuButton[];
  matchrule: ConditionalMatchRule;
}): Promise<{ menuid: string }> {
  const accessToken = await params.tokenHandle.getAccessToken();
  const data = await jsonRequest<{ menuid?: string }>({
    method: "POST",
    endpoint: "cgi-bin/menu/addconditional",
    query: { access_token: accessToken },
    body: {
      button: params.buttons,
      matchrule: params.matchrule,
    },
    network: params.account.network,
  });
  return { menuid: String(data.menuid ?? "") };
}

export async function deleteConditionalMenu(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  menuid: string;
}): Promise<void> {
  const accessToken = await params.tokenHandle.getAccessToken();
  await jsonRequest({
    method: "POST",
    endpoint: "cgi-bin/menu/delconditional",
    query: { access_token: accessToken },
    body: { menuid: params.menuid },
    network: params.account.network,
  });
}

export async function tryMatchConditionalMenu(params: {
  account: ResolvedWechatServiceAccount;
  tokenHandle: AccessTokenHandle;
  user_id: string;
}): Promise<Record<string, unknown>> {
  const accessToken = await params.tokenHandle.getAccessToken();
  return jsonRequest<Record<string, unknown>>({
    method: "POST",
    endpoint: "cgi-bin/menu/trymatch",
    query: { access_token: accessToken },
    body: { user_id: params.user_id },
    network: params.account.network,
  });
}
