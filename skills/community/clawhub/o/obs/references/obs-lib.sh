#!/bin/bash
# obs-lib.sh - OBS API Library
# OBS API 库函数

set -e

# ============================================================================
# 配置 | Configuration
# ============================================================================

OBS_APIURL="${OBS_APIURL:-https://api.opensuse.org}"
OBS_USERNAME="${OBS_USERNAME:-}"
OBS_TOKEN="${OBS_TOKEN:-}"

# 从 oscrc 读取配置 | Read config from oscrc
if [ -f "$HOME/.config/osc/oscrc" ]; then
    OSCRC_APIURL=$(grep -E "^apiurl\s*=" "$HOME/.config/osc/oscrc" | head -1 | cut -d'=' -f2 | tr -d ' ')
    OBS_APIURL="${OSCRC_APIURL:-$OBS_APIURL}"
fi

# ============================================================================
# 认证 | Authentication
# ============================================================================

obs_auth_header() {
    if [ -n "$OBS_USERNAME" ] && [ -n "$OBS_TOKEN" ]; then
        echo "-u $OBS_USERNAME:$OBS_TOKEN"
    elif command -v osc &> /dev/null && [ -f "$HOME/.config/osc/oscrc" ]; then
        echo "--cookie-jar /tmp/obs_cookie_$$ --cookie /tmp/obs_cookie_$$"
    else
        echo ""
    fi
}

obs_api_call() {
    local method="$1"
    local endpoint="$2"
    local data="$3"
    local content_type="${4:-application/xml}"
    
    local url="${OBS_APIURL}${endpoint}"
    local auth=$(obs_auth_header)
    
    local curl_opts="-s -X ${method}"
    [ -n "$auth" ] && curl_opts="$curl_opts $auth"
    curl_opts="$curl_opts -H 'Content-Type: ${content_type}'"
    
    if [ -n "$data" ]; then
        if [[ "$data" == @* ]]; then
            curl_opts="$curl_opts --data-binary \"$data\""
        else
            curl_opts="$curl_opts -d \"$data\""
        fi
    fi
    
    eval "curl $curl_opts \"$url\""
}

obs_api_call_raw() {
    local method="$1"
    local endpoint="$2"
    shift 2
    
    local url="${OBS_APIURL}${endpoint}"
    local auth=$(obs_auth_header)
    
    if [ -n "$auth" ]; then
        curl -s -X "${method}" $auth "$@" "$url"
    else
        curl -s -X "${method}" "$@" "$url"
    fi
}

# ============================================================================
# 项目操作 | Project Operations
# ============================================================================

obs_project_get() {
    local project="$1"
    obs_api_call "GET" "/source/$project"
}

obs_project_meta() {
    local project="$1"
    obs_api_call "GET" "/meta/project/$project"
}

obs_project_create() {
    local project="$1"
    local title="$2"
    local description="$3"
    
    local xml="<project name=\"$project\">
  <title>$title</title>
  <description>$description</description>
  <person role=\"maintainer\" userid=\"$OBS_USERNAME\"/>
</project>"
    
    obs_api_call "PUT" "/meta/project/$project" "$xml"
}

obs_project_delete() {
    local project="$1"
    obs_api_call "DELETE" "/source/$project"
}

obs_project_list_packages() {
    local project="$1"
    obs_api_call "GET" "/source/$project?view=packages"
}

# ============================================================================
# 包操作 | Package Operations
# ============================================================================

obs_package_get() {
    local project="$1"
    local package="$2"
    obs_api_call "GET" "/source/$project/$package"
}

obs_package_meta() {
    local project="$1"
    local package="$2"
    obs_api_call "GET" "/meta/package/$project/$package"
}

obs_package_create() {
    local project="$1"
    local package="$2"
    local description="${3:-Package $package}"
    
    local xml="<package name=\"$package\" project=\"$project\">
  <title>$package</title>
  <description>$description</description>
</package>"
    
    obs_api_call "PUT" "/meta/package/$project/$package" "$xml"
}

obs_package_delete() {
    local project="$1"
    local package="$2"
    obs_api_call "DELETE" "/source/$project/$package"
}

obs_package_checkout() {
    local project="$1"
    local package="$2"
    local output_dir="${3:-$package}"
    
    mkdir -p "$output_dir"
    local files=$(obs_package_list_files "$project" "$package" | grep -oP '(?<=name=")[^"]+')
    
    for file in $files; do
        obs_file_get "$project" "$package" "$file" > "$output_dir/$file"
    done
}

obs_package_list_files() {
    local project="$1"
    local package="$2"
    obs_api_call "GET" "/source/$project/$package"
}

# ============================================================================
# 文件操作 | File Operations
# ============================================================================

obs_file_get() {
    local project="$1"
    local package="$2"
    local file="$3"
    local rev="${4:-}"
    
    local endpoint="/source/$project/$package/$file"
    [ -n "$rev" ] && endpoint="$endpoint?rev=$rev"
    
    obs_api_call_raw "GET" "$endpoint"
}

obs_file_upload() {
    local project="$1"
    local package="$2"
    local file="$3"
    local message="${4:-Upload file}"
    
    local filename=$(basename "$file")
    local endpoint="/source/$project/$package/$filename?comment=$(urlencode "$message")"
    
    obs_api_call_raw "PUT" "$endpoint" --data-binary "@$file"
}

obs_file_delete() {
    local project="$1"
    local package="$2"
    local file="$3"
    local message="${4:-Delete file}"
    
    local endpoint="/source/$project/$package/$file?comment=$(urlencode "$message")"
    obs_api_call "DELETE" "$endpoint"
}

obs_file_list() {
    local project="$1"
    local package="$2"
    obs_api_call "GET" "/source/$project/$package"
}

# ============================================================================
# 构建操作 | Build Operations
# ============================================================================

obs_build_status() {
    local project="$1"
    local package="$2"
    obs_api_call "GET" "/build/$project/_result?package=$package"
}

obs_build_rebuild() {
    local project="$1"
    local package="$2"
    local repository="$3"
    local arch="$4"
    
    local endpoint="/build/$project/$repository/$arch/$package?cmd=rebuild"
    obs_api_call "POST" "$endpoint"
}

obs_build_log() {
    local project="$1"
    local package="$2"
    local repository="$3"
    local arch="$4"
    local last_failed="${5:-}"
    
    local endpoint="/build/$project/$repository/$arch/$package/logs"
    [ -n "$last_failed" ] && endpoint="$endpoint?lastfail=1"
    
    obs_api_call_raw "GET" "$endpoint"
}

obs_build_stop() {
    local project="$1"
    local package="$2"
    local repository="$3"
    local arch="$4"
    
    local endpoint="/build/$project/$repository/$arch/$package?cmd=stopbuild"
    obs_api_call "POST" "$endpoint"
}

obs_build_results() {
    local project="$1"
    local package="$2"
    obs_api_call "GET" "/build/$project/_result?package=$package&view=status"
}

# ============================================================================
# 提交请求 | Submit Requests
# ============================================================================

obs_request_create() {
    local source_project="$1"
    local source_package="$2"
    local target_project="$3"
    local target_package="$4"
    local description="${5:-}"
    
    local xml="<request type=\"submit\">
  <action>
    <submit>
      <source project=\"$source_project\" package=\"$source_package\"/>
      <target project=\"$target_project\" package=\"$target_package\"/>
    </submit>
  </action>
  <description>$description</description>
</request>"
    
    obs_api_call "POST" "/request" "$xml"
}

obs_request_get() {
    local request_id="$1"
    obs_api_call "GET" "/request/$request_id"
}

obs_request_list() {
    local project="${1:-}"
    local states="${2:-new,review,accepted,declined}"
    
    local endpoint="/request"
    local params="states=$states"
    [ -n "$project" ] && params="$params&project=$project"
    
    obs_api_call "GET" "$endpoint?$params"
}

obs_request_accept() {
    local request_id="$1"
    local message="${2:-}"
    
    local endpoint="/request/$request_id?cmd=accept"
    [ -n "$message" ] && endpoint="$endpoint&message=$(urlencode "$message")"
    
    obs_api_call "POST" "$endpoint"
}

obs_request_reject() {
    local request_id="$1"
    local message="${2:-}"
    
    local endpoint="/request/$request_id?cmd=decline"
    [ -n "$message" ] && endpoint="$endpoint&message=$(urlencode "$message")"
    
    obs_api_call "POST" "$endpoint"
}

obs_request_revoke() {
    local request_id="$1"
    local message="${2:-}"
    
    local endpoint="/request/$request_id?cmd=revoke"
    [ -n "$message" ] && endpoint="$endpoint&message=$(urlencode "$message")"
    
    obs_api_call "POST" "$endpoint"
}

# ============================================================================
# 搜索 | Search
# ============================================================================

obs_search_projects() {
    local query="$1"
    obs_api_call "GET" "/search/project?match=@name~'$query'"
}

obs_search_packages() {
    local query="$1"
    local project="${2:-}"
    
    local endpoint="/search/package?match=@name~'$query'"
    [ -n "$project" ] && endpoint="$endpoint&project=$project"
    
    obs_api_call "GET" "$endpoint"
}

# ============================================================================
# 工具函数 | Utility Functions
# ============================================================================

urlencode() {
    local string="$1"
    local strlen=${#string}
    local encoded=""
    
    for (( pos = 0 ; pos < strlen ; pos++ )); do
        c=${string:$pos:1}
        case "$c" in
            [-_.~a-zA-Z0-9] ) o="${c}" ;;
            * ) printf -v o '%%%02X' "'$c" ;;
        esac
        encoded+="${o}"
    done
    echo "${encoded}"
}

obs_xml_pretty() {
    if command -v xmllint &> /dev/null; then
        xmllint --format -
    else
        cat
    fi
}

obs_json_output() {
    local format="${1:-xml}"
    if [ "$format" = "json" ] && command -v xml2json &> /dev/null; then
        xml2json
    else
        cat
    fi
}

# ============================================================================
# 认证测试 | Authentication Test
# ============================================================================

obs_auth_test() {
    local response=$(obs_api_call "GET" "/person/$OBS_USERNAME" 2>&1)
    if echo "$response" | grep -q "status=\"complete\""; then
        echo "✓ Authentication successful | 认证成功"
        return 0
    else
        echo "✗ Authentication failed | 认证失败"
        echo "Response: $response"
        return 1
    fi
}
