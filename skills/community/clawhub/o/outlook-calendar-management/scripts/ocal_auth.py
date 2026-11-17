"""ocal_auth — 认证与 token：token 文件读写、自动续期、跨进程续期锁。"""
import contextlib
import os, json, time

from ocal_errors import CalError
from ocal_i18n import t

# An explicit credential file isolates test/account sessions from the default login.
TOKEN_PATH = os.path.abspath(os.path.expanduser(
    os.environ.get("OCAL_TOKEN_PATH", "~/.outlook_cal_token.json")))

# 权限清单：日历读写 + 邮箱设置读取（全天日程按邮箱首选时区写入用）。
# Azure 应用注册侧另有 User.Read（设备码登录的基础权限，返回登录用户身份）；
# 老版本 token 只有 Calendars.ReadWrite，读 mailboxSettings 会 403，
# 上层已做静默回退——但建议用户重跑 outlook_setup.py 拿到新权限。
SCOPES = ("Calendars.ReadWrite", "MailboxSettings.Read")


@contextlib.contextmanager
def _token_lock():
    """跨进程续期锁（非阻塞，拿不到就跳过）。

    两个终端同时续期时，双方拿到的 refresh token 都有效（最后写者胜），
    锁的意义是避免重复请求与文件交叉写；拿不到锁直接继续，不影响正确性。

    :yield: 锁持有期间执行续期与写文件
    """
    path = TOKEN_PATH + ".lock"
    try:
        fd = os.open(path, os.O_CREAT | os.O_RDWR, 0o600)
    except OSError:
        yield  # 锁文件都建不了（只读目录等），跳过锁
        return
    acquired = False
    try:
        if os.name == "nt":
            import msvcrt
            try:
                if os.fstat(fd).st_size == 0:
                    os.write(fd, b"\0")  # msvcrt 锁至少要锁住 1 字节
                msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
                acquired = True
            except OSError:
                pass
        else:
            import fcntl
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                acquired = True
            except OSError:
                pass
        yield
    finally:
        try:
            if acquired:
                if os.name == "nt":
                    import msvcrt
                    os.lseek(fd, 0, 0)
                    msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(fd, fcntl.LOCK_UN)
        except OSError:
            pass
        os.close(fd)


def setup_hint():
    """认证引导文案（跟随当前语言）。

    不能做成常量：语言可能在模块导入之后才被设置（--lang 在 main 里才解析）。

    :return: 提示用户怎么跑认证的字符串
    """
    return t("setup_hint")


# ── 认证 ──────────────────────────────────────────

def get_token():
    """拿一个能用的访问令牌：没过期直接返回，过期了用 refresh token 续。

    :return: access token 字符串；还没认证过返回 None
    :raises CalError: token 文件损坏 / 没有 refresh token / 续期失败
    """
    if not os.path.exists(TOKEN_PATH):
        return None
    try:
        with open(TOKEN_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        raise CalError(t("err_token_corrupt", hint=setup_hint()))
    expires_at = data.get('expires_at', 0)
    access_token = data.get('access_token')
    if access_token and expires_at and expires_at > time.time() + 300:
        return access_token
    refresh_token = data.get('refresh_token')
    if not refresh_token:
        raise CalError(t("err_no_refresh", hint=setup_hint()))
    client_id = data.get('client_id') or os.environ.get('OUTLOOK_CLIENT_ID', '')
    if not client_id:
        raise CalError(t("err_no_client_id", hint=setup_hint()))
    with _token_lock():
        # 双检：拿到锁后重读文件，另一个进程可能刚刚续好并写回
        try:
            with open(TOKEN_PATH, 'r', encoding='utf-8') as f:
                data2 = json.load(f)
            at2 = data2.get('access_token')
            if at2 and data2.get('expires_at', 0) > time.time() + 300:
                return at2
        except (OSError, json.JSONDecodeError):
            pass
        return _refresh_token(refresh_token, client_id, data.get('_authority', 'consumers'))


def _refresh_token(refresh_token, client_id, authority):
    """用 refresh token 换新的 access token，并把结果写回 token 文件。

    :param refresh_token: 上次存下来的 refresh token
    :param client_id: 应用 ID（续期必须和认证时一致）
    :param authority: 账户类型（consumers 或 common）
    :return: 新的 access token
    :raises CalError: 缺 msal 库 / refresh token 失效 / 其他刷新失败
    """
    try:
        from msal import PublicClientApplication
    except ImportError:
        raise CalError(t("err_no_msal"))
    app = PublicClientApplication(client_id, authority=f"https://login.microsoftonline.com/{authority}")
    result = app.acquire_token_by_refresh_token(refresh_token, scopes=list(SCOPES))
    if 'access_token' in result:
        result['refresh_token'] = result.get('refresh_token', refresh_token)
        result['expires_at'] = time.time() + result.get('expires_in', 3600)
        result['_authority'] = authority
        result['client_id'] = client_id
        # 先写临时文件再原子替换：写入中途崩溃不会把 token 文件写坏成半截 JSON
        tmp = TOKEN_PATH + ".tmp"
        try:
            with open(tmp, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False)
            try:
                os.chmod(tmp, 0o600)  # token 含 access/refresh token，收紧权限
            except OSError:
                pass
            os.replace(tmp, TOKEN_PATH)
        finally:
            try:
                os.unlink(tmp)
            except OSError:
                pass
        return result['access_token']
    error = result.get('error', 'unknown')
    desc = result.get('error_description', '')
    if error == 'invalid_grant':
        raise CalError(t("err_refresh_invalid"))
    raise CalError(t("err_refresh_fail", error=error, desc=desc[:200]))
