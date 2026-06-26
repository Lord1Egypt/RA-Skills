#!/usr/bin/env bash
set -euo pipefail

package="${ANALYTICSCLI_CLI_PACKAGE:-@analyticscli/cli}"
home_dir="${HOME:-$(pwd)}"
user_prefix="${ANALYTICSCLI_NPM_PREFIX:-${home_dir}/.local}"

path_entries_for() {
  local bin_dir="$1"
  local entries=()

  entries+=("${bin_dir}")
  if [[ "${bin_dir}" == "${home_dir}/.local/bin" ]]; then
    entries+=("${home_dir}/.local/analyticscli-npm/bin")
  fi

  local entry
  local rendered=()
  for entry in "${entries[@]}"; do
    if [[ "${entry}" == "${home_dir}/"* ]]; then
      rendered+=("\$HOME/${entry#"${home_dir}/"}")
    else
      rendered+=("${entry}")
    fi
  done

  local joined="${rendered[0]}"
  for entry in "${rendered[@]:1}"; do
    joined="${joined}:${entry}"
  done
  printf '%s' "${joined}"
}

print_path_hint() {
  local bin_dir="$1"
  local path_entries
  path_entries="$(path_entries_for "${bin_dir}")"
  cat <<EOF
analyticscli was installed into:
  ${bin_dir}

For future shells, make sure this directory is on PATH:
  export PATH="${path_entries}:\$PATH"

For the current shell/session, run:
  export PATH="${path_entries}:\$PATH"

Or reload your shell profile:
  source "${home_dir}/.bashrc" 2>/dev/null || source "${home_dir}/.profile"
EOF
}

ensure_profile_path() {
  local bin_dir="$1"
  local path_entries
  path_entries="$(path_entries_for "${bin_dir}")"
  local line="export PATH=\"${path_entries}:\$PATH\""
  local wrote_any=false

  if [[ "${ANALYTICSCLI_SKIP_PROFILE_UPDATE:-}" == "true" ]]; then
    return 0
  fi

  for profile in "${home_dir}/.profile" "${home_dir}/.bashrc" "${home_dir}/.bash_profile" "${home_dir}/.zshrc" "${home_dir}/.zprofile"; do
    if [[ ! -f "${profile}" ]]; then
      : >"${profile}"
    fi
    if ! grep -Fq "${line}" "${profile}"; then
      printf '\n# AnalyticsCLI CLI user-local npm bin\n%s\n' "${line}" >>"${profile}"
      wrote_any=true
    fi
  done

  if [[ "${wrote_any}" == "true" ]]; then
    echo "Added ${path_entries} to shell profile files. Already-open terminals still need: export PATH=\"${path_entries}:\$PATH\"" >&2
  fi
}

verify_fresh_shell() {
  local shell_path="$1"
  local source_script="$2"
  local clean_path="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"

  if [[ ! -x "${shell_path}" ]]; then
    return 1
  fi

  env HOME="${home_dir}" PATH="${clean_path}" "${shell_path}" -lc "${source_script}" >/dev/null 2>&1
}

verify_profile_path() {
  local bin_dir="$1"
  local bash_probe='for f in "$HOME/.bash_profile" "$HOME/.bashrc" "$HOME/.profile"; do [[ -f "$f" ]] && source "$f" >/dev/null 2>&1 || true; done; command -v analyticscli >/dev/null 2>&1 && analyticscli --help >/dev/null 2>&1'
  local zsh_probe='for f in "$HOME/.zprofile" "$HOME/.zshrc" "$HOME/.profile"; do [[ -f "$f" ]] && source "$f" >/dev/null 2>&1 || true; done; command -v analyticscli >/dev/null 2>&1 && analyticscli --help >/dev/null 2>&1'
  local sh_probe='[ -f "$HOME/.profile" ] && . "$HOME/.profile" >/dev/null 2>&1 || true; command -v analyticscli >/dev/null 2>&1 && analyticscli --help >/dev/null 2>&1'

  if verify_fresh_shell /bin/bash "${bash_probe}" || \
    verify_fresh_shell /usr/bin/bash "${bash_probe}" || \
    verify_fresh_shell /bin/zsh "${zsh_probe}" || \
    verify_fresh_shell /usr/bin/zsh "${zsh_probe}" || \
    verify_fresh_shell /bin/sh "${sh_probe}" || \
    verify_fresh_shell /usr/bin/sh "${sh_probe}"; then
    echo "Fresh shell verification passed for analyticscli via ${bin_dir}" >&2
    return 0
  fi

  echo "analyticscli works in this installer process, but fresh shell verification failed after updating profile files." >&2
  print_path_hint "${bin_dir}" >&2
  return 1
}

if ! command -v npm >/dev/null 2>&1; then
  if command -v analyticscli >/dev/null 2>&1; then
    echo "analyticscli already available: $(command -v analyticscli)"
    echo "npm is not available, so the package update check was skipped." >&2
    analyticscli --help >/dev/null
    exit 0
  fi
  echo "npm is required to install ${package}, but npm was not found." >&2
  exit 1
fi

echo "Ensuring AnalyticsCLI CLI from npm package ${package}"
set +e
global_output="$(npm install -g "${package}" 2>&1)"
global_exit=$?
set -e

if [[ ${global_exit} -ne 0 ]]; then
  if printf '%s' "${global_output}" | grep -Eiq 'EACCES|permission denied|access denied|operation not permitted'; then
    echo "Global npm install failed because of permissions. Falling back to user-local prefix: ${user_prefix}" >&2
    mkdir -p "${user_prefix}"
    npm install -g --prefix "${user_prefix}" "${package}"
    export PATH="${user_prefix}/bin:${PATH}"
    ensure_profile_path "${user_prefix}/bin"
  else
    printf '%s\n' "${global_output}" >&2
    exit "${global_exit}"
  fi
fi

if ! command -v analyticscli >/dev/null 2>&1; then
  echo "Installed ${package}, but analyticscli is still not on PATH." >&2
  if [[ -x "${user_prefix}/bin/analyticscli" ]]; then
    print_path_hint "${user_prefix}/bin" >&2
  else
    echo "Check your npm global bin directory with: npm prefix -g" >&2
  fi
  exit 1
fi

echo "analyticscli available: $(command -v analyticscli)"
analyticscli --help >/dev/null
case "$(command -v analyticscli)" in
  "${user_prefix}/bin/"*)
    ensure_profile_path "${user_prefix}/bin"
    verify_profile_path "${user_prefix}/bin"
    print_path_hint "${user_prefix}/bin"
    ;;
esac
