"""OK.com CSS 选择器集中管理

所有 CSS 选择器在此统一维护，避免散落在各模块中。
ok.com 使用 React SSR，部分 class 带有 hash 后缀，可能随版本更新变化。
"""

# ─── 搜索 ─────────────────────────────────────────────────
SEARCH_INPUT = "#custom-input"
SEARCH_BUTTON = "button[class*='searchButton']"

# ─── 列表页 ─────────────────────────────────────────────────
# 首页推荐卡片
LISTING_CARD_HOME = ".home-recommend-item-card"
# 列表页（搜索/分类）卡片
LISTING_CARD_LIST = "a[class*='item-card-default']"
# 通用：二者之一
LISTING_CARD = f"{LISTING_CARD_HOME}, {LISTING_CARD_LIST}"
# 卡片内部元素
CARD_TITLE = "[class*='itemTitle'], [class*='card-title'], h3"
CARD_PRICE = "[class*='itemPrice'], [class*='card-price'], [class*='price']"
CARD_LOCATION = "[class*='itemLocation'], [class*='card-location'], [class*='location']"
CARD_IMAGE = "img"

# ─── 详情页 ─────────────────────────────────────────────────
DETAIL_TITLE = "h1"
DETAIL_PRICE = "[class*='price'], [class*='Price']"
DETAIL_DESCRIPTION = "[class*='description'], [class*='Description'], [class*='detail-content']"
DETAIL_SELLER = (
    "[class*='agencyUserInfoName'], [class*='AgencyCard'] [class*='Name'], "
    "[class*='seller'], [class*='Seller'], [class*='user-name']"
)
DETAIL_LOCATION = "[class*='location'], [class*='Location'], [class*='address']"
DETAIL_IMAGES = "img[loading='lazy']"
DETAIL_TIME = "[class*='time'], [class*='Time'], [class*='date']"
DETAIL_FEATURE_ITEM = "[class*='MainInfo_item'], [class*='featureItem'], [class*='FeatureItem']"
DETAIL_FEATURE_VALUE = "[class*='value'], [class*='Value']"
DETAIL_CATEGORY = "[class*='Breadcrumb'] a, [class*='breadcrumb'] a"
DETAIL_CONTACT_BTN = "[class*='applyButton'], [class*='contact'], button[class*='message']"

# ─── 导航/头部 ─────────────────────────────────────────────
NAV_BROWSE_MENU = "[class*='browse'], [class*='Browse']"
NAV_CATEGORY_ITEMS = "[class*='dropdownItemLabel'], [class*='categoryItem']"
BREADCRUMB = "[class*='Breadcrumb'] a, [class*='breadcrumb'] a"

# ─── 城市选择器 ─────────────────────────────────────────────
# 筛选栏上的城市 filter（列表页顶部，文本为当前城市名）
# 用 __ 后缀精确匹配容器 div，排除 filterItemIcon/Content/Point 等子元素
CITY_FILTER_ITEM = "[class*='FilterItem_filterItem__']"
# 城市搜索弹出面板（点击城市 filter 后展开）
CITY_SEARCH_OVERLAY = "[class*='FilterItemPC_newLocationOverlay']"
CITY_SEARCH_INPUT = "input[placeholder='Search City']"
CITY_SEARCH_RESULT_ITEM = "[class*='LocationWrapperNew_searchResultItem']"
CITY_SEARCH_RESULT_NAME = "[class*='LocationWrapperNew_resultName']"
CITY_SEARCH_RESULT_ADDR = "[class*='LocationWrapperNew_resultAddress']"

# ─── 国家/语言选择器 ─────────────────────────────────────────
COUNTRY_SELECTOR_TRIGGER = "[class*='flagIcon'], [class*='flag-icon']"
COUNTRY_CHANGE_BTN = "[class*='changeCountry'], [class*='change-country']"

# ─── 首页分类图标 ─────────────────────────────────────────────
HOMEPAGE_CATEGORY_LINK = "a[href*='/cate-']"
HOMEPAGE_CATEGORY_ICON = "a[href*='/cate-'], [class*='categoryIcon'], [class*='category-icon']"
# QuickAccessArea：首页可见的分类快捷入口行（Marketplace / Jobs / Property / Cars …）
HOMEPAGE_QUICK_ACCESS_ITEM = "a[class*='QuickAccessArea_item__']"

# ─── 筛选/排序 ─────────────────────────────────────────────
FILTER_SORT = "[class*='sortFilter'], [class*='sort-filter']"
# 筛选条上的 FilterItem 按钮（文本匹配 "Price"）
FILTER_ITEM = "[class*='FilterItem_filterItem__']"
# Price 面板（点击 Price 按钮后展开的浮层）
FILTER_PRICE_OVERLAY = "[class*='FilterItemPC_filterItemOverlay']"
# 价格输入框
FILTER_PRICE_MIN = "input.native-numeric-input[placeholder='Min']"
FILTER_PRICE_MAX = "input.native-numeric-input[placeholder='Max']"
# 筛选浮层底部的 Confirm/Clear 按钮
FILTER_CONFIRM_BTN = "button[type='submit'][class*='FilterItemPC_button']"
FILTER_CLEAR_BTN = "button[type='reset'][class*='FilterItemPC_button']"

# ─── 分页/加载更多 ─────────────────────────────────────────
LOAD_MORE_BTN = "[class*='loadMore'], [class*='load-more'], button[class*='more']"
PAGINATION = "[class*='pagination'], [class*='Pagination']"

# ─── Cookie 横幅 ─────────────────────────────────────────
COOKIE_BANNER = "[class*='cookie'], [class*='Cookie']"
COOKIE_ACCEPT_BTN = "[class*='cookie'] button, [class*='Cookie'] button"

# ─── 顶部导航栏 ─────────────────────────────────────────────
# Favourites 入口在顶部导航栏（非头像下拉）
NAV_FAVOURITES_WRAPPER = "[class*='TopBarRightContent_iconImgWrapper']"
NAV_FAVOURITES_TEXT = "[class*='TopBarRightContent_text']"

# ─── 用户菜单（头像下拉） ─────────────────────────────────
USER_MENU_TRIGGER = "[class*='PcUserInfo_userInfoArea']"
USER_MENU_POPOVER = "[class*='HoverPopup_customPopover']"
USER_MENU_ITEM = "[class*='PcUserInfo_textItemWrapper']"
USER_MENU_ITEM_TEXT = "[class*='PcUserInfo_textItem']"

# ─── 收藏页（/biz/en/list/favorites） ─────────────────────
FAV_PAGE_TITLE = ".page-title"
FAV_LIST_WRAPPER = ".list-components-list-wraper"
FAV_CARD = (
    "a[class*='list-components-item-card-default-a']"
)
FAV_CARD_TITLE = ".title"
FAV_CARD_PRICE = ".prices"
FAV_CARD_IMAGE = ".image-container img"
FAV_CARD_ADDRESS = ".address"
FAV_CARD_COMPANY = ".jobCardCompany"
# 卡片上的心形收藏按钮（列表页 & 收藏页通用）
FAV_HEART_BTN = ".list-components-item-favorite.pc-card"
FAV_HEART_ICON = ".favorite-icon"

# ─── 详情页收藏按钮 ─────────────────────────────────────────
DETAIL_FAV_AREA = "[class*='MainInfo_favAndShare']"
DETAIL_FAV_BTN = "[class*='PcImageOperationArea_imgWrapper']"

# ─── 我的帖子页（/biz/en/publish/list） ─────────────────────
MY_POST_PAGE = ".page-list-page"
MY_POST_CONTAINER = ".page-list-container"
MY_POST_LIST = ".list-container"
MY_POST_CATE_TABS = ".tab-bar.cate .tab"
MY_POST_STATE_TABS = ".tab-bar.state .tab"
MY_POST_EMPTY = ".list-empty"
MY_POST_CARD = ".pc-list-item"
MY_POST_CARD_TITLE = ".item-content-title"
MY_POST_CARD_PRICE = ".item-content-price"
MY_POST_CARD_IMAGE = ".item-img-container img"
MY_POST_CARD_ADDRESS = ".item-content-address"
MY_POST_CARD_STATS = ".item-statistics"
MY_POST_ACTION_BTN = ".pc-list-item-handle"
MY_POST_DROPDOWN = ".dropdown-menu"
MY_POST_DROPDOWN_ITEM = ".dropdown-item"

# ─── 登录相关 ─────────────────────────────────────────────
LOGIN_BTN = "[class*='login'], [class*='Login'], [class*='signIn']"
USER_AVATAR = "[class*='avatar'], [class*='Avatar'], [class*='userIcon']"
USER_NAME = "[class*='userName'], [class*='user-name']"

# ─── 登录弹窗流程 ─────────────────────────────────────────
# PC 顶栏（宽屏）；窄屏 / 移动 UA 时可能整段不出现，需配合 login.py 内文本兜底
LOGIN_TRIGGER = "#pcUserInfoArea [class*='PcUserInfo_loginButton']"
# 不依赖 #pcUserInfoArea，只要页面上有该类名即可（部分布局下父级 id 不同）
LOGIN_TRIGGER_ANY = "[class*='PcUserInfo_loginButton']"
LOGIN_MODAL = "[class*='LoginPC_loginContainer']"
LOGIN_MODAL_CLOSE = "[class*='TopBar_closeBtn']"
LOGIN_MODAL_BACK = "[class*='TopBar_backBtn']"

# 第一步：邮箱输入
LOGIN_EMAIL_INPUT = ".ok_login_input_label_content_input"
LOGIN_CONTINUE_BTN = "[class*='ValidAccount_loginBtn']"
LOGIN_CLEAR_INPUT = ".ok_login_input_label_suffix_clear"

# 第二步：密码输入
# 已注册用户登录页使用 CustomCounterInput，注册页使用 ok_login_input
LOGIN_PASSWORD_INPUT_LOGIN = "[class*='CustomCounterInput_customInput']"
LOGIN_PASSWORD_INPUT_REGISTER = ".ok_login_input_label_content_input"
LOGIN_SUBMIT_BTN = "[class*='LoginPC_continueButton'], [class*='ValidAccount_loginBtn']"

# 页面标题（区分登录 vs 注册）
LOGIN_TITLE_WELCOME = "[class*='WelcomeTip_welcomeTitle']"
LOGIN_TITLE_REGISTER = "[class*='ValidAccount_title']"

# 忘记密码
LOGIN_FORGOT_PASSWORD = "[class*='LoginPC_forgottenPassword']"

# 第三方登录图标
SOCIAL_LOGIN_GOOGLE = "[class*='SocialLoginIcons'] img[alt='google']"
SOCIAL_LOGIN_FACEBOOK = "[class*='SocialLoginIcons'] img[alt='facebook']"
SOCIAL_LOGIN_APPLE = "[class*='SocialLoginIcons'] img[alt='apple']"

# 登录错误提示
LOGIN_ERROR_MSG = "[class*='errorMsg'], [class*='error-msg'], [class*='ErrorTip']"

# 已登录状态（非 login 按钮，说明已登录）
LOGGED_IN_INDICATOR = "[class*='PcUserInfo_userInfoArea'] [class*='avatar'], [class*='PcUserInfo_userInfoArea'] img[class*='Avatar']"
