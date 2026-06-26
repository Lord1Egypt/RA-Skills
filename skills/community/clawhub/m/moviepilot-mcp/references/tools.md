# MoviePilot MCP 工具完整参考

共 70 个工具，按类别分组。调用方式见 SKILL.md。

> 配置信息（服务器地址、API Key）通过 `config.json` 管理，不硬编码在任何文件中。

## 搜索与识别

### search_media

Search TMDB database for media resources (movies, TV shows, anime, etc.) by title, year, type, and other criteria. Returns detailed media information from TMDB. Use 'recognize_media' to extract info from torrent titles/file paths, or 'scrape_metadata' to generate metadata files.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| title | string | ✓ | The title of the media to search for (e.g., 'The Matrix', 'Breaking Bad') |
| year | string |  | Release year of the media (optional, helps narrow down results) |
| media_type | string |  | Allowed values: movie, tv |
| season | integer |  | Season number for TV shows and anime (optional, only applicable for series) |

---

### search_person

Search for person information including actors, directors, etc. Supports searching by name. Returns detailed person information from TMDB, Douban, or Bangumi database.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| name | string | ✓ | The name of the person to search for (e.g., 'Tom Hanks', '周杰伦') |

---

### search_person_credits

Search for films and TV shows that a person/actor has appeared in (filmography). Supports searching by person ID from TMDB, Douban, or Bangumi database. Returns a list of media works the person has participated in.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| person_id | integer | ✓ | The ID of the person/actor to search for credits (e.g., 31 for Tom Hanks in TMDB) |
| source | string | ✓ | The data source: 'tmdb' for TheMovieDB, 'douban' for Douban, 'bangumi' for Bangumi |
| page | integer |  | Page number for pagination (default: 1) |

---

### recognize_media

Extract/identify media information from torrent titles or file paths (NOT database search). Supports two modes: 1) Extract from torrent title and optional subtitle, 2) Extract from file path. Returns detailed media information. Use 'search_media' to search TMDB database, or 'scrape_metadata' to generate metadata files for existing files.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| title | string |  | The title of the torrent/media to recognize (required for torrent recognition) |
| subtitle | string |  | The subtitle or description of the torrent (optional, helps improve recognition accuracy) |
| path | string |  | The file path to recognize (required for file recognition, mutually exclusive with title) |

---

### query_media_detail

Query supplementary media details from TMDB by ID and media_type. Accepts tmdb_id or douban_id (at least one required). media_type accepts 'movie' or 'tv'. Returns non-duplicated detail fields such as status, genres, directors, actors, and season info for TV series.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| tmdb_id | integer |  | TMDB ID of the media (movie or TV series, can be obtained from search_media tool) |
| douban_id | string |  | Douban ID of the media (alternative to tmdb_id) |
| media_type | string | ✓ | Allowed values: movie, tv |

---

### query_episode_schedule

Query TV series episode air dates and schedule. Returns non-duplicated schedule fields, including episode list, air-date statistics, and per-episode metadata. Filters out episodes without air dates.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| tmdb_id | integer | ✓ | TMDB ID of the TV series (can be obtained from search_media tool) |
| season | integer | ✓ | Season number to query |
| episode_group | string |  | Episode group ID (optional) |

---

### get_recommendations

Get trending and popular media recommendations from various sources. Returns curated lists of popular movies, TV shows, and anime based on different criteria like trending, ratings, or calendar schedules. Supports pagination with 20 items per page.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| source | string |  | Recommendation source: 'tmdb_trending' for TMDB trending content, 'tmdb_movies' for TMDB popular movies, 'tmdb_tvs' for TMDB popular TV shows, 'douban_hot' for Douban popular content, 'douban_movie_hot' for Douban hot movies, 'douban_tv_hot' for Douban hot TV shows, 'douban_movie_showing' for Douban movies currently showing, 'douban_movies' for Douban latest movies, 'douban_tvs' for Douban latest TV shows, 'douban_movie_top250' for Douban movie TOP250, 'douban_tv_weekly_chinese' for Douban Chinese TV weekly chart, 'douban_tv_weekly_global' for Douban global TV weekly chart, 'douban_tv_animation' for Douban popular animation, 'bangumi_calendar' for Bangumi anime calendar |
| media_type | string |  | Allowed values: movie, tv, all |
| page | integer |  | Page number for pagination (default: 1, 20 items per page) |

---

## 订阅管理

### add_subscribe

Add media subscription to create automated download rules for movies and TV shows. The system will automatically search and download new episodes or releases based on the subscription criteria. For TV shows, omitting `season` subscribes season 1 only by default; to subscribe multiple seasons or the full series, call this tool once per season. Supports advanced filtering options like quality, resolution, and effect filters using regular expressions.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| title | string | ✓ | The title of the media to subscribe to (e.g., 'The Matrix', 'Breaking Bad') |
| year | string | ✓ | Release year of the media (required for accurate identification) |
| media_type | string | ✓ | Allowed values: movie, tv |
| season | integer |  | Season number for TV shows (optional). If omitted, the subscription defaults to season 1 only. To subscribe multiple seasons or the full series, call this tool separately for each season. |
| tmdb_id | integer |  | TMDB database ID for precise media identification (optional, can be obtained from search_media tool) |
| douban_id | string |  | Douban ID for precise media identification (optional, alternative to tmdb_id) |
| start_episode | integer |  | Starting episode number for TV shows (optional, defaults to 1 if not specified) |
| total_episode | integer |  | Total number of episodes for TV shows (optional, will be auto-detected from TMDB if not specified) |
| quality | string |  | Quality filter as regular expression (optional, e.g., 'BluRay|WEB-DL|HDTV') |
| resolution | string |  | Resolution filter as regular expression (optional, e.g., '1080p|720p|2160p') |
| effect | string |  | Effect filter as regular expression (optional, e.g., 'HDR|DV|SDR') |
| filter_groups | array |  | List of filter rule group names to apply (optional, can be obtained from query_rule_groups tool) |
| sites | array |  | List of site IDs to search from (optional, can be obtained from query_sites tool) |

---

### update_subscribe

Update subscription properties including filters, episode counts, state, and other settings. Supports updating quality/resolution filters, episode tracking, subscription state, and download configuration.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| subscribe_id | integer | ✓ | The ID of the subscription to update (can be obtained from query_subscribes tool) |
| name | string |  | Subscription name/title (optional) |
| year | string |  | Release year (optional) |
| season | integer |  | Season number for TV shows (optional) |
| total_episode | integer |  | Total number of episodes (optional) |
| lack_episode | integer |  | Number of missing episodes (optional) |
| start_episode | integer |  | Starting episode number (optional) |
| quality | string |  | Quality filter as regular expression (optional, e.g., 'BluRay|WEB-DL|HDTV') |
| resolution | string |  | Resolution filter as regular expression (optional, e.g., '1080p|720p|2160p') |
| effect | string |  | Effect filter as regular expression (optional, e.g., 'HDR|DV|SDR') |
| include | string |  | Include filter as regular expression (optional) |
| exclude | string |  | Exclude filter as regular expression (optional) |
| filter | string |  | Filter rule as regular expression (optional) |
| state | string |  | Subscription state: 'R' for enabled, 'P' for pending, 'S' for paused (optional) |
| sites | array |  | List of site IDs to search from (optional) |
| downloader | string |  | Downloader name (optional) |
| save_path | string |  | Save path for downloaded files (optional) |
| best_version | integer |  | Whether to upgrade to best version: 0 for no, 1 for yes (optional) |
| best_version_full | integer |  | For TV best-version subscriptions, only download full-season packs: 0 for no, 1 for yes (optional) |
| custom_words | string |  | Custom recognition words (optional) |
| media_category | string |  | Custom media category (optional) |
| episode_group | string |  | Episode group ID (optional) |

---

### search_subscribe

Search for missing episodes/resources for a specific subscription. This tool will search torrent sites for the missing episodes of the subscription and automatically download matching resources. Use this when a user wants to search for missing episodes of a specific subscription.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| subscribe_id | integer | ✓ | The ID of the subscription to search for missing episodes (can be obtained from query_subscribes tool) |
| manual | boolean |  | Whether this is a manual search (default: False) |
| filter_groups | array |  | List of filter rule group names to apply for this search (optional, can be obtained from query_rule_groups tool. If provided, will temporarily update the subscription's filter groups before searching) |

---

### query_subscribes

Query subscription status and list user subscriptions. Returns full subscription parameters for each matched subscription. Supports pagination with 100 items per page.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| status | string |  | Filter subscriptions by status: 'R' for enabled subscriptions, 'S' for paused ones, 'all' for all subscriptions |
| media_type | string |  | Allowed values: movie, tv, all |
| tmdb_id | integer |  | Filter by TMDB ID to check if a specific media is already subscribed |
| douban_id | string |  | Filter by Douban ID to check if a specific media is already subscribed |
| page | integer |  | Page number for pagination (default: 1, 100 items per page) |

---

### query_subscribe_shares

Query shared subscriptions from other users. Shows popular subscriptions shared by the community with filtering and pagination support.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| name | string |  | Filter shares by media name (partial match, optional) |
| page | integer |  | Page number for pagination (default: 1) |
| count | integer |  | Number of items per page (default: 30, max: 50) |
| genre_id | integer |  | Filter by genre ID (optional) |
| min_rating | number |  | Minimum rating filter (optional, e.g., 7.5) |
| max_rating | number |  | Maximum rating filter (optional, e.g., 10.0) |
| sort_type | string |  | Sort type (optional, e.g., 'count', 'rating') |

---

### query_popular_subscribes

Query popular subscriptions based on user shared data. Shows media with the most subscribers, supports filtering by genre, rating, minimum subscribers, and pagination.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| media_type | string | ✓ | Allowed values: movie, tv |
| page | integer |  | Page number for pagination (default: 1) |
| count | integer |  | Number of items per page (default: 30, max: 50) |
| min_sub | integer |  | Minimum number of subscribers filter (optional, e.g., 5) |
| genre_id | integer |  | Filter by genre ID (optional) |
| min_rating | number |  | Minimum rating filter (optional, e.g., 7.5) |
| max_rating | number |  | Maximum rating filter (optional, e.g., 10.0) |
| sort_type | string |  | Sort type (optional, e.g., 'count', 'rating') |

---

### query_subscribe_history

Query subscription history records. Shows completed subscriptions with their details including name, type, rating, completion date, and other subscription information. Supports filtering by media type and name. Supports pagination with 20 records per page.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| media_type | string |  | Allowed values: movie, tv, all |
| name | string |  | Filter by media name (partial match, optional) |
| page | integer |  | Page number for pagination (default: 1, 20 items per page). Ignored when name filter is provided. |

---

### delete_subscribe

Delete a media subscription by its ID. This will remove the subscription and stop automatic downloads for that media.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| subscribe_id | integer | ✓ | The ID of the subscription to delete (can be obtained from query_subscribes tool) |

---

## 下载管理

### search_torrents

Search for torrent files by media ID across configured indexer sites, cache the matched results, and return available filter options for follow-up selection. Requires tmdb_id or douban_id (can be obtained from search_media tool) for accurate matching.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| tmdb_id | integer |  | TMDB ID (can be obtained from search_media tool). Either tmdb_id or douban_id must be provided. |
| douban_id | string |  | Douban ID (can be obtained from search_media tool). Either tmdb_id or douban_id must be provided. |
| media_type | string |  | Allowed values: movie, tv |
| area | string |  | Search scope: 'title' (default) or 'imdbid' |
| sites | array |  | Array of specific site IDs to search on (optional, if not provided searches all configured sites) |

---

### get_search_results

Get cached torrent search results from search_torrents with optional filters. Supports pagination with up to 50 results per page.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| site | array |  | Site name filters |
| season | array |  | Season or episode filters |
| free_state | array |  | Promotion state filters |
| video_code | array |  | Video codec filters |
| edition | array |  | Edition filters |
| resolution | array |  | Resolution filters |
| release_group | array |  | Release group filters |
| title_pattern | string |  | Regular expression pattern to filter torrent titles (e.g., '4K|2160p|UHD', '1080p.*BluRay') |
| show_filter_options | boolean |  | Whether to return only optional filter options for re-checking available conditions |
| page | integer |  | Page number for pagination (default: 1, each page returns up to 50 results) |

---

### add_download

Add torrent download tasks using refs from get_search_results or magnet links.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| torrent_url | array | ✓ | One or more torrent_url values. Supports refs from get_search_results (`hash:id`) and magnet links. |
| downloader | string |  | Name of the downloader to use (optional, uses default if not specified) |
| save_path | string |  | Directory path where the downloaded files should be saved. Using `<storage>:<path>` for remote storage. e.g. rclone:/MP, smb:/server/share/Movies. (optional, uses default path if not specified) |
| labels | string |  | Comma-separated list of labels/tags to assign to the download (optional, e.g., 'movie,hd,bluray') |

---

### query_download_tasks

Query download status and list download tasks. Can query all active downloads, or search for specific tasks by hash, title, or tag. Shows download progress, completion status, tags, and task details from configured downloaders.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| downloader | string |  | Name of specific downloader to query (optional, if not provided queries all configured downloaders) |
| status | string |  | Filter downloads by status: 'downloading' for active downloads, 'completed' for finished downloads, 'paused' for paused downloads, 'all' for all downloads |
| hash | string |  | Query specific download task by hash (optional, if provided will search for this specific task regardless of status) |
| title | string |  | Query download tasks by title/name (optional, supports partial match, searches all tasks if provided) |
| tag | string |  | Filter download tasks by tag (optional, supports partial match, e.g. 'movie' will match tasks with tag 'movie' or 'movie_2024') |

---

### modify_download

Modify a download task in the downloader by task hash. Supports: 1) Setting tags on a download task, 2) Starting (resuming) a paused download task, 3) Stopping (pausing) a downloading task. Multiple operations can be performed in a single call.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| hash | string | ✓ | Task hash (can be obtained from query_download_tasks tool) |
| action | string |  | Action to perform on the task: 'start' to resume downloading, 'stop' to pause downloading. If not provided, no start/stop action will be performed. |
| tags | array |  | List of tags to set on the download task. If provided, these tags will be added to the task. Example: ['movie', 'hd'] |
| downloader | string |  | Name of specific downloader (optional, if not provided will search all downloaders) |

---

### delete_download

Delete a download task from the downloader by task hash only. Optionally specify the downloader name and whether to delete downloaded files.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| hash | string | ✓ | Task hash (can be obtained from query_download_tasks tool) |
| downloader | string |  | Name of specific downloader (optional, if not provided will search all downloaders) |
| delete_files | boolean |  | Whether to delete downloaded files along with the task (default: False, only removes the task from downloader) |

---

### delete_download_history

Delete a download history record by ID. This only removes the record from the database, does not delete any actual files.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| history_id | integer | ✓ | The ID of the download history record to delete |

---

### query_downloaders

Query downloader configuration and list all available downloaders. Shows downloader status, connection details, and configuration settings.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |

---

## 媒体库整理

### query_library_exists

Check whether media already exists in Plex, Emby, or Jellyfin by media ID. Results are grouped by media server; TV results include existing episodes, total episodes, and missing episodes/seasons. Requires tmdb_id or douban_id from search_media.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| tmdb_id | integer |  | TMDB ID (can be obtained from search_media tool). Either tmdb_id or douban_id must be provided. |
| douban_id | string |  | Douban ID (can be obtained from search_media tool). Either tmdb_id or douban_id must be provided. |
| media_type | string |  | Allowed values: movie, tv |

---

### query_library_latest

Query the latest media items added to the media server (Plex, Emby, Jellyfin). Returns recently added movies and TV series with their titles, images, links, and other metadata. Supports pagination with 20 items per page.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| server | string |  | Media server name (optional, if not specified queries all enabled media servers) |
| page | integer |  | Page number for pagination (default: 1, 20 items per page) |

---

### scrape_metadata

Generate metadata files (NFO files, posters, backgrounds, etc.) for existing media files or directories. Automatically recognizes media information from the file path and creates metadata files. Supports both local and remote storage. Use 'search_media' to search TMDB database, or 'recognize_media' to extract info from torrent titles/file paths without generating files.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| path | string | ✓ | Path to the file or directory to scrape metadata for (e.g., '/path/to/file.mkv' or '/path/to/directory') |
| storage | string |  | Storage type: 'local' for local storage, 'smb', 'alist', etc. for remote storage (default: 'local') |
| overwrite | boolean |  | Whether to overwrite existing metadata files (default: False) |

---

### transfer_file

Transfer/organize a file or directory to the media library. Automatically recognizes media information and organizes files according to configured rules. Supports custom target paths, media identification, and transfer modes.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| file_path | string | ✓ | Path to the file or directory to transfer (e.g., '/path/to/file.mkv' or '/path/to/directory') |
| storage | string |  | Storage type of the source file (default: 'local', can be 'smb', 'alist', etc.) |
| target_path | string |  | Target path for the transferred file/directory (optional, uses default library path if not specified) |
| target_storage | string |  | Target storage type (optional, uses default storage if not specified) |
| media_type | string |  | Allowed values: movie, tv |
| tmdbid | integer |  | TMDB ID for precise media identification (optional but recommended for accuracy) |
| doubanid | string |  | Douban ID for media identification (optional) |
| season | integer |  | Season number for TV shows (optional) |
| transfer_type | string |  | Transfer mode: 'move' to move files, 'copy' to copy files, 'link' for hard link, 'softlink' for symbolic link (optional, uses default mode if not specified) |
| background | boolean |  | Whether to run transfer in background (default: False, runs synchronously) |

---

### query_transfer_history

Query file transfer history records. Shows transfer status, source and destination paths, media information, and transfer details. Supports filtering by title and status.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| title | string |  | Search by title (optional, supports partial match) |
| status | string |  | Filter by status: 'success' for successful transfers, 'failed' for failed transfers, 'all' for all records (default: 'all') |
| page | integer |  | Page number for pagination (default: 1, each page contains 30 records) |

---

### delete_transfer_history

Delete a specific transfer history record by its ID. This is useful when you need to remove a failed transfer record before retrying the transfer, as the system skips files that already have transfer history.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| history_id | integer | ✓ | The ID of the transfer history record to delete |

---

### query_directory_settings

Query system directory configuration settings (NOT file listings). Returns configured directory paths, storage types, transfer modes, and other directory-related settings. Use 'list_directory' to list actual files and folders in a directory.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| directory_type | string |  | Filter directories by type: 'download' for download directories, 'library' for media library directories, 'all' for all directories |
| storage_type | string |  | Filter directories by storage type: 'local' for local storage, 'remote' for remote storage, 'all' for all storage types |
| name | string |  | Filter directories by name (partial match, optional) |

---

### list_directory

List actual files and folders in a file system directory (NOT configuration). Shows files and subdirectories with their names, types, sizes, and modification times. Returns up to 20 items and the total count if there are more items. Use 'query_directory_settings' to query directory configuration settings.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| path | string | ✓ | Directory path to list contents (e.g., '/home/user/downloads' or 'C:/Downloads') |
| storage | string |  | Storage type (default: 'local' for local file system, can be 'smb', 'alist', etc.) |
| sort_by | string |  | Sort order: 'name' for alphabetical sorting, 'time' for modification time sorting (default: 'name') |

---

## 站点管理

### query_sites

Query site status and list all configured sites. Shows site name, domain, status, priority, and basic configuration. Site priority (pri): smaller values have higher priority (e.g., pri=1 has higher priority than pri=10).

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| status | string |  | Filter sites by status: 'active' for enabled sites, 'inactive' for disabled sites, 'all' for all sites |
| name | string |  | Filter sites by name (partial match, optional) |

---

### update_site

Update site configuration including URL, priority, authentication credentials (cookie, UA, API key), proxy settings, rate limits, and other site properties. Supports updating multiple site attributes at once. Site priority (pri): smaller values have higher priority (e.g., pri=1 has higher priority than pri=10).

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| site_id | integer | ✓ | The ID of the site to update (can be obtained from query_sites tool) |
| name | string |  | Site name (optional) |
| url | string |  | Site URL (optional, will be automatically formatted) |
| pri | integer |  | Site priority (optional, smaller value = higher priority, e.g., pri=1 has higher priority than pri=10) |
| rss | string |  | RSS feed URL (optional) |
| cookie | string |  | Site cookie (optional) |
| ua | string |  | User-Agent string (optional) |
| apikey | string |  | API key (optional) |
| token | string |  | API token (optional) |
| proxy | integer |  | Whether to use proxy: 0 for no, 1 for yes (optional) |
| filter | string |  | Filter rule as regular expression (optional) |
| note | string |  | Site notes/remarks (optional) |
| timeout | integer |  | Request timeout in seconds (optional, default: 15) |
| limit_interval | integer |  | Rate limit interval in seconds (optional) |
| limit_count | integer |  | Rate limit count per interval (optional) |
| limit_seconds | integer |  | Rate limit seconds between requests (optional) |
| is_active | boolean |  | Whether site is active: True for enabled, False for disabled (optional) |
| downloader | string |  | Downloader name for this site (optional) |

---

### query_site_userdata

Query user data for a specific site including username, user level, upload/download statistics, seeding information, bonus points, and other account details. Supports querying data for a specific date or latest data.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| site_id | integer | ✓ | The ID of the site to query user data for (can be obtained from query_sites tool) |
| workdate | string |  | Work date to query (optional, format: 'YYYY-MM-DD', if not specified returns latest data) |

---

### test_site

Test site connectivity and availability. This will check if a site is accessible and can be logged in. Accepts site ID only.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| site_identifier | integer | ✓ | Site ID to test (can be obtained from query_sites tool) |

---

### update_site_cookie

Update site Cookie and User-Agent by logging in with username and password. This tool can automatically obtain and update the site's authentication credentials. Supports two-step verification for sites that require it. Accepts site ID only.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| site_identifier | integer | ✓ | Site ID to update Cookie and User-Agent for (can be obtained from query_sites tool) |
| username | string | ✓ | Site login username |
| password | string | ✓ | Site login password |
| two_step_code | string |  | Two-step verification code or secret key (optional, required for sites with 2FA enabled) |

---

## 过滤规则

### query_builtin_filter_rules

Query built-in filter rules defined by the backend filter module. These rule IDs can be used directly inside rule_string expressions for filter rule groups. Use this tool before add_rule_group or update_rule_group to learn valid built-in rule IDs.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| rule_ids | array |  | Optional list of built-in rule IDs to query. If omitted, return all built-in rules. |

---

### query_custom_filter_rules

Query custom filter rules stored in CustomFilterRules. Custom rules can be referenced from rule_string expressions in filter rule groups. Use this tool before add_rule_group or update_rule_group to learn valid custom rule IDs.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| rule_ids | array |  | Optional list of custom rule IDs to query. If omitted, return all custom rules. |
| include_group_refs | boolean |  | Whether to include which rule groups reference each custom rule. |

---

### query_rule_groups

Query filter rule groups (过滤规则组 / 优先级规则组). Each rule group contains a rule_string made of built-in rules and/or custom rules. Inside one level use '&', '|', '!' and optional parentheses; use '>' between levels. Levels are evaluated from left to right, and the first matched level wins. The result includes parsed levels and syntax guidance so the agent can learn existing patterns before writing a new rule group.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| group_names | array |  | Optional list of rule group names to query. If omitted, return all rule groups. |
| include_usage | boolean |  | Whether to include where each rule group is referenced by global settings or subscriptions. |

---

### add_custom_filter_rule

Add a custom filter rule to CustomFilterRules. The new rule can then be referenced by rule ID inside filter rule groups.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| rule_id | string | ✓ | Unique custom rule ID. Only letters and numbers are allowed. |
| name | string | ✓ | Display name of the custom rule. |
| include | string |  | Optional include regex for the rule. |
| exclude | string |  | Optional exclude regex for the rule. |
| size_range | string |  | Optional size range in MB, for example '1000-5000'. |
| seeders | string |  | Optional minimum seeder count as a non-negative integer. |
| publish_time | string |  | Optional publish-time filter in minutes, for example '60' or '60-1440'. |

---

### update_custom_filter_rule

Update an existing custom filter rule. If the rule ID is renamed, all rule groups that reference the old ID are updated automatically.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| current_rule_id | string | ✓ | Existing custom rule ID to update. |
| new_rule_id | string |  | New rule ID. If omitted, keep the original rule ID. |
| name | string |  | New display name. If omitted, keep the original name. |
| include | string |  | New include regex. Pass an empty string to clear it. |
| exclude | string |  | New exclude regex. Pass an empty string to clear it. |
| size_range | string |  | New size range in MB. Pass an empty string to clear it. |
| seeders | string |  | New minimum seeder count. Pass an empty string to clear it. |
| publish_time | string |  | New publish-time filter in minutes. Pass an empty string to clear it. |

---

### delete_custom_filter_rule

Delete a custom filter rule from CustomFilterRules. If the rule is still referenced by rule groups, the deletion is blocked to avoid breaking rule_string expressions.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| rule_id | string | ✓ | Custom rule ID to delete. |

---

### add_rule_group

Add a new filter rule group to UserFilterRuleGroups. Rule groups are matched level by level from left to right and can be linked to search/subscription flows. Before calling this tool, first use query_builtin_filter_rules and query_custom_filter_rules to confirm valid rule IDs, and optionally use query_rule_groups to imitate existing rule_string patterns.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| name | string | ✓ | New rule group name. |
| rule_string | string | ✓ | Rule expression using built-in/custom rule IDs. Use '&', '!' inside one level, and use '>' between priority levels. Example: 'SPECSUB & CNVOI & 4K & !BLU > CNSUB & CNVOI & 4K & !BLU'. |
| media_type | string |  | Optional media type scope: '电影', '电视剧', 'movie', or 'tv'. |
| category | string |  | Optional media category. Only valid when media_type is set. |

---

### update_rule_group

Update a filter rule group. If the rule group name changes, its references in global search/subscription settings and per-subscription bindings are updated automatically. Before changing rule_string, first use query_builtin_filter_rules and query_custom_filter_rules to confirm valid rule IDs.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| current_name | string | ✓ | Existing rule group name to update. |
| new_name | string |  | New rule group name. If omitted, keep the original name. |
| rule_string | string |  | New rule_string. If omitted, keep the original rule_string. Example: 'SPECSUB & CNVOI & 4K & !BLU > CNSUB & CNVOI & 4K & !BLU'. |
| media_type | string |  | New media type scope. Pass an empty string to clear it. |
| category | string |  | New category. Pass an empty string to clear it. |

---

### delete_rule_group

Delete a filter rule group from UserFilterRuleGroups. The tool also removes dangling references from global settings and subscriptions.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| name | string | ✓ | Rule group name to delete. |

---

## 插件管理

### query_installed_plugins

Query installed plugins in MoviePilot. Returns all installed plugins or filters them by keywords. Use this tool to find the exact plugin_id before uninstall_plugin or other plugin management tools are used.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| query | string |  | Optional keyword to filter installed plugins by plugin ID, name, description, or author. |
| max_results | integer |  | Maximum number of plugins to return. Defaults to 50, capped at 200. |

---

### query_market_plugins

Query available plugins from the plugin market and local plugin repositories. Can return the full plugin list or filter by keywords before install_plugin is used.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| query | string |  | Optional keyword to filter plugin market results by plugin ID, name, description, or author. |
| max_results | integer |  | Maximum number of plugins to return. Defaults to 50, capped at 200. |
| force_refresh | boolean |  | Whether to refresh plugin market caches before querying. |

---

### query_plugin_capabilities

Query the capabilities of installed plugins, including supported commands and scheduled services. Commands are slash-commands (e.g. /xxx) that can be executed via the run_slash_command tool. Scheduled services are periodic tasks that can be triggered via the run_scheduler tool. Optionally specify a plugin_id to query a specific plugin, or omit to query all running plugins.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| plugin_id | string |  | Optional plugin ID to query capabilities for a specific plugin. If not provided, returns capabilities of all running plugins. Use query_installed_plugins tool to get the plugin IDs first. |

---

### query_plugin_config

Query the saved configuration of an installed plugin. Returns the current saved config and, when available, the plugin's default config model. Use this before update_plugin_config so you only change the intended keys.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| plugin_id | string | ✓ | The plugin ID to query. Use query_installed_plugins first to discover valid plugin IDs. |

---

### update_plugin_config

Update the saved configuration of an installed plugin. By default this performs a partial merge update and does NOT reload the plugin automatically. Call reload_plugin afterwards to apply the latest saved config to the running plugin.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| plugin_id | string | ✓ | The plugin ID to update. Use query_plugin_config first to inspect the current config. |
| updates | object |  | Config items to save. By default this tool merges these keys into the existing config instead of replacing the whole config. |
| remove_keys | array |  | Optional config keys to remove from the saved plugin config. |
| replace | boolean |  | Whether to replace the entire saved config with 'updates'. Default false, which performs a partial merge update. |

---

### reload_plugin

Reload an installed plugin so its latest saved configuration takes effect. This also refreshes the plugin's registered commands, scheduled services, and API routes.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| plugin_id | string | ✓ | The plugin ID to reload so the latest saved config takes effect. |

---

### query_plugin_data

Query persisted data of an installed plugin. Optionally specify a key to read a single data item; otherwise all plugin data entries are returned. When the result is too large, the tool automatically truncates it and returns a preview instead.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| plugin_id | string | ✓ | The plugin ID to query. Use query_installed_plugins first to discover valid plugin IDs. |
| key | string |  | Optional plugin data key. If omitted, returns all plugin data entries for the plugin. |
| max_chars | integer |  | Maximum number of preview characters to return when plugin data is too large. Default 12000, capped at 50000. |

---

### install_plugin

Install a plugin by exact plugin_id from the plugin market or local plugin repositories. Use query_market_plugins first when you need filtering or discovery.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| plugin_id | string | ✓ | Exact plugin ID to install. Use query_market_plugins first to find the correct plugin_id. |
| force | boolean |  | Whether to force reinstall or upgrade the specified plugin. |
| force_refresh_market | boolean |  | Whether to refresh plugin market caches before reading the market list. |

---

### uninstall_plugin

Uninstall an installed plugin by exact plugin_id. Use query_installed_plugins first when you need filtering or discovery.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| plugin_id | string | ✓ | Exact plugin ID to uninstall. Use query_installed_plugins first to find the correct plugin_id. |

---

## 系统与自动化

### query_schedulers

Query scheduled tasks and list all available scheduler jobs. Shows job status, next run time, and provider information.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |

---

### run_scheduler

Manually trigger a scheduled task to run immediately. This will execute the specified scheduler job by its ID.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| job_id | string | ✓ | The ID of the scheduled job to run (can be obtained from query_schedulers tool) |

---

### query_workflows

Query workflow list and status. Shows workflow name, description, trigger type, state, execution count, and other workflow details. Supports filtering by state, name, and trigger type.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| state | string |  | Filter workflows by state: 'W' for waiting, 'R' for running, 'P' for paused, 'S' for success, 'F' for failed, 'all' for all workflows (default: 'all') |
| name | string |  | Filter workflows by name (partial match, optional) |
| trigger_type | string |  | Filter workflows by trigger type: 'timer' for scheduled, 'event' for event-triggered, 'manual' for manual, 'all' for all types (default: 'all') |

---

### run_workflow

Execute a specific workflow manually by workflow ID. Supports running from the beginning or continuing from the last executed action.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| workflow_id | integer | ✓ | Workflow ID (can be obtained from query_workflows tool) |
| from_begin | boolean |  | Whether to run workflow from the beginning (default: True, if False will continue from last executed action) |

---

### query_system_settings

Query system settings across both the basic Settings module and all SystemConfig-backed categories. Use this tool to inspect downloaders, media servers, notification channels, storages, directories, search-site ranges, subscribe-site ranges, site auth params, AI agent config, and any other system setting before making changes.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| setting_key | string |  | Exact setting key to query. Supports Settings field names like 'APP_DOMAIN' or 'TMDB_API_KEY', SystemConfigKey values like 'Downloaders' or 'MediaServers', enum names, and some single-key aliases such as 'downloaders', 'directories', 'search_sites', 'subscribe_sites', 'site_auth', 'ai_agent', and 'custom_identifiers'. |
| group | string |  | Optional group filter when setting_key is not provided. Supports 'all', 'settings', 'systemconfig', and category aliases such as 'downloaders', 'media_servers', 'notifications', 'notification_switches', 'storages', 'directories', 'search_sites', 'subscribe_sites', 'site_auth', 'ai_agent', 'filter_rules', 'subscribe_defaults', 'plugins', and 'custom_identifiers'. Chinese aliases are also accepted. |
| keyword | string |  | Optional keyword used to fuzzy match setting keys, group names, or labels when listing settings. |
| include_values | boolean |  | Whether to include full setting values. Default behavior: when a single setting is matched it returns the full value; when multiple settings are matched it returns summaries only unless this is explicitly set to true. |

---

### update_system_settings

Update system settings across both the basic Settings module and all SystemConfig-backed categories. Supports full replacement, shallow dict merge, and generic list item upsert/remove so the agent can manage downloaders, media servers, notification channels, storages, directories, search-site ranges, subscribe-site ranges, site auth params, AI agent config, and other system settings through one tool.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| setting_key | string | ✓ | Exact setting key to update. Supports Settings field names, SystemConfigKey values, enum names, and common aliases such as 'downloaders', 'directories', 'search_sites', 'subscribe_sites', 'site_auth', 'ai_agent', and 'custom_identifiers'. |
| value | array |  | The new value or list item payload. For replace: this becomes the entire setting value. For merge_dict: this should be a dict of keys to merge. For upsert_list_item/remove_list_item: this can be a dict item or a scalar list item. |
| operation | string |  | Update operation. replace replaces the whole value; merge_dict merges dict keys (optionally with remove_keys); upsert_list_item inserts or replaces one item inside a list; remove_list_item removes one item from a list. |
| remove_keys | array |  | Optional dict keys to delete when operation is merge_dict. |
| match_field | string |  | Optional match field for list item upsert/remove. If omitted, common SystemConfig categories use built-in defaults such as 'name' or 'type'. |
| match_value | array |  | Optional explicit value used to locate a list item when operation is upsert_list_item or remove_list_item. |

---

### query_personas

List all available personas (人格) and show which one is currently active. Use this before switching persona when the user asks for a different speaking style but does not name an exact persona_id. The result includes persona_id, label, description, aliases, and whether it is active.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| query | string |  | Optional search keyword for persona_id, label, description, or aliases. Use this when the user asks for a certain speaking style but the exact persona name is unknown. |

---

### switch_persona

Switch the active persona (人格) used by the agent runtime. This change is persistent for future turns. Use this when the user explicitly asks to change the speaking style, tone, or response persona. If the user asks for a vague style and you are not sure which persona matches best, call query_personas first.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| persona_id | string | ✓ | The target persona to activate. This can be the exact persona_id, label, or one of the persona aliases. If the exact persona is unclear, call query_personas first. |

---

### update_persona_definition

Create or update a runtime persona definition (人格定义) without manually editing PERSONA.md files. Use this when the user explicitly asks to modify how a persona is defined, such as changing tone rules, rewriting the persona body, adjusting aliases, or creating a new persona.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| persona_id | string | ✓ | Target persona to update. For existing personas this can be persona_id, label, or alias. For new personas, provide the new lowercase persona_id. |
| label | string |  | Optional new label shown to users, such as 默认 or 说明型. |
| description | string |  | Optional short description of the persona's intended style. |
| aliases | array |  | Optional full replacement list of aliases for this persona. |
| instructions | string |  | Optional full replacement body for PERSONA.md, excluding YAML frontmatter. Use this when the persona definition should be rewritten completely. |
| append_instructions | array |  | Optional extra persona rules to append to the existing PERSONA body. Use this for small adjustments such as '回答更短' or '复杂问题给两步解释'. |
| create_if_missing | boolean |  | Whether to create a new runtime persona if the target persona does not already exist. |

---

### list_slash_commands

List all available slash commands in the system, including system preset commands (e.g. /cookiecloud, /sites, /subscribes, /downloading, /transfer, /restart, etc.) and plugin-registered commands. Use this tool to discover what slash commands are available before executing them with run_slash_command. This is especially useful when the user describes an action in natural language and you need to find the matching command to fulfill their request.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |

---

### run_slash_command

Execute a slash command (system or plugin) by sending a CommandExcute event. This tool supports ALL registered slash commands, including: 1) System preset commands (e.g. /cookiecloud, /sites, /subscribes, /downloading, /transfer, /restart, etc.) 2) Plugin commands registered by installed plugins. Use the query_plugin_capabilities tool to discover plugin commands, or the list_slash_commands tool to discover all available commands. The command will be executed asynchronously. Note: This tool triggers the command execution but the actual processing happens in the background.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| command | string | ✓ | The slash command to execute, e.g. '/cookiecloud'. Must start with '/'. Can include arguments after the command, e.g. '/command arg1 arg2'. Use query_plugin_capabilities tool to discover available plugin commands, or list_slash_commands tool to discover all available commands (including system commands). |

---

### query_custom_identifiers

Query all currently configured custom identifiers (自定义识别词). Returns the list of identifier rules used for preprocessing torrent/file names before media recognition. Use this tool to check existing rules before adding new ones to avoid duplicates.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |

---

### update_custom_identifiers

Update the full list of custom identifiers (自定义识别词) used for preprocessing torrent/file names. This tool REPLACES all existing identifier rules with the provided list. IMPORTANT: Always use 'query_custom_identifiers' first to get existing rules, then merge new rules into the list before calling this tool to avoid accidentally deleting existing rules. IMPORTANT: New identifier rules are global. When the rule is created from a specific torrent/file name, make the regex as narrow as possible and include distinctive elements from that sample so unrelated titles are not affected. Prefer contextual replacements with capture groups/backreferences over bare block words when a generic word like REPACK, WEB-DL, 1080p, 字幕, or a simple episode marker would otherwise match too broadly. Supported rule formats (spaces around operators are required): 1) Block word: just the word/regex to remove; 2) Replacement: '被替换词 => 替换词'; 3) Episode offset: '前定位词 <> 后定位词 >> EP±N'; 4) Combined: '被替换词 => 替换词 && 前定位词 <> 后定位词 >> EP±N'; Lines starting with '#' are comments. The replacement target supports: {[tmdbid=xxx;type=movie/tv;g=xxx;s=xxx;e=xxx]} for direct TMDB ID matching; g is an optional TMDB episode group ID for TV recognition.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| identifiers | array | ✓ | The complete list of custom identifier rules to save. This REPLACES the entire existing list. Always query existing identifiers first, merge new rules, then pass the full list. These rules are global and affect future recognition for all torrents/files. When adding a rule for a user-provided sample, prefer narrow regex patterns that include sample-specific anchors such as the title alias, year, season/episode marker, group tag, resolution, or other distinctive fragments. Avoid overly broad patterns like bare generic tags, pure episode numbers, or common release words unless the user explicitly wants a global rule. |

---

### send_message

Send notification message to the user through configured notification channels (Telegram, Slack, WeChat, etc.). Supports optional image_url on channels that can send images. Used to inform users about operation results, errors, important updates, or proactively send a relevant image.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this tool is being used in the current context |
| message | string |  | The message content to send to the user (should be clear and informative) |
| title | string |  | Title of the message, a short summary of the message content |
| image_url | string |  | Optional image URL to send together with the message on channels that support images (such as Telegram and Slack) |

---

### send_local_file

Send a local image or file from the server filesystem to the current user. Use this when you have generated or identified a local file the user should download.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why sending this local file helps the user |
| file_path | string | ✓ | Absolute path to the local image or file to send to the user |
| message | string |  | Optional message or caption to send with the attachment |
| title | string |  | Optional short title shown together with the attachment |
| file_name | string |  | Optional override filename presented to the user when downloading |

---

### browse_webpage

Control a real browser (Playwright) to interact with web pages. Supports navigating to URLs, reading page content, taking screenshots, clicking elements, filling forms, selecting dropdown options, executing JavaScript, and waiting for elements. Use this tool when you need to interact with dynamic web pages, fill in forms, click buttons, or extract content from JavaScript-rendered pages. The browser session persists across multiple calls within the same conversation - first call 'goto' to open a page, then use other actions to interact with it.

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| explanation | string |  | Clear explanation of why this browser action is being performed |
| action | string | ✓ | The browser action to perform. Available actions: - 'goto': Navigate to a URL, returns page title and text summary - 'get_content': Get current page content (text or HTML) - 'screenshot': Take a screenshot of the current page, returns base64 image - 'click': Click on an element specified by selector - 'fill': Fill text into an input element specified by selector - 'select': Select an option from a dropdown element - 'evaluate': Execute JavaScript code on the page and return the result - 'wait': Wait for an element to appear on the page |
| url | string |  | URL to navigate to (required for 'goto' action) |
| selector | string |  | CSS selector or text selector for the target element (for 'click', 'fill', 'select', 'wait' actions). Supports CSS selectors like '#id', '.class', 'tag', and Playwright text selectors like 'text=Click me' |
| value | string |  | Value to fill into input or option value to select (for 'fill' and 'select' actions) |
| script | string |  | JavaScript code to execute on the page (for 'evaluate' action). The script should return a value that can be serialized to JSON. |
| content_type | string |  | Content type for 'get_content' action: 'text' for readable text, 'html' for raw HTML |
| timeout | integer |  | Timeout in seconds for the action (default: 30) |
| cookies | string |  | Cookies to set for the browser context, format: 'name1=value1; name2=value2' |
| user_agent | string |  | Custom User-Agent string for the browser context |

---
