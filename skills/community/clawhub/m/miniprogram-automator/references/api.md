# Full API Reference

## automator.launch

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| cliPath | string | no | auto-detected | DevTools CLI absolute path |
| projectPath | string | yes | - | Project absolute path |
| timeout | number | no | 30000 | Max launch wait (ms) |
| port | number | no | - | WebSocket port |
| account | string | no | - | User openid (multi-account) |
| projectConfig | Object | no | - | Override project.config.json |
| ticket | string | no | - | Login ticket |

## automator.connect

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| wsEndpoint | string | yes | DevTools WebSocket address |

CLI start automation: `cli --auto <project_root> --auto-port <port>`

## MiniProgram Methods

| Method | Returns | Required Params | Description |
|--------|---------|----------------|-------------|
| pageStack | Array | - | Page stack |
| navigateTo(url) | Page | url | Keep current page, navigate |
| redirectTo(url) | Page | url | Close current page, navigate |
| navigateBack() | - | - | Go back |
| reLaunch(url) | Page | url | Close all pages, navigate |
| switchTab(url) | Page | url | Switch to tabBar |
| currentPage() | Page | - | Current page |
| systemInfo() | Object | - | System info |
| callWxMethod(m,...a) | any | method | Call wx method |
| callPluginWxMethod(m,...a) | any | - | Call plugin wx method |
| mockWxMethod(m,result) | - | method, result | Override wx method |
| mockPluginWxMethod(m,r) | - | - | Override plugin wx method |
| restoreWxMethod(m) | - | method | Restore wx method |
| restorePluginWxMethod(m) | - | - | Restore plugin wx method |
| evaluate(fn,...a) | any | fn(str) | Inject code snippet |
| pageScrollTo(st) | - | scrollTop(px) | Scroll to position |
| screenshot(opts) | string|Buffer | - | Screenshot |
| exposeFunction(n,fn) | - | name, fn | Expose method to mini program |
| testAccounts() | Array | - | Multi-account user list |
| stopAudits(opts) | Report | - | Stop performance audit |
| getTicket() | {ticket,expiredTime} | - | Get login ticket |
| setTicket(ticket) | - | ticket | Set login ticket |
| refreshTicket() | - | - | Refresh ticket |
| remote(opts) | - | - | Remote debugging |
| disconnect() | - | - | Disconnect |
| close() | - | - | Disconnect and close window |

## MiniProgram Events

| Event | Parameter | Description |
|-------|-----------|-------------|
| console | {type, args} | Triggered on console output |
| exception | {message, stack} | Triggered on JS error |

## Page

| Property/Method | Params | Returns | Description |
|----------------|--------|---------|-------------|
| .path | - | string | Page path |
| .query | - | Object | Page parameters |
| $(selector) | selector | Element|null | Get element |
| $$(selector) | selector | Element[] | Get elements |
| waitFor(cond) | s/n/Fn | - | Wait for condition |
| data(path) | path(opt) | any | Page render data |
| setData(data) | data(Object) | - | Set render data |
| size() | - | {w,h} | Scrollable size |
| scrollTop() | - | number | Scroll position |
| callMethod(m,...) | method,args | - | Call page method |

## Element

| Method | Params | Returns | Description |
|--------|--------|---------|-------------|
| .tagName | - | string | Tag name |
| $(sel) | selector | Element\|null | Find child element |
| $$(sel) | selector | Element[] | Find child elements |
| size() | - | {w,h} | Element size |
| offset() | - | {l,t} | Absolute position(px) |
| text() | - | string | Text content |
| attribute(n) | name | string | Tag attribute |
| property(n) | name | any | DOM property |
| wxml() | - | string | WXML |
| outerWxml() | - | string | WXML+self |
| value() | - | any | Element value |
| style(n) | name | string | Computed style |
| tap() | - | - | Tap |
| longpress() | - | - | Long press |
| input(v) | value | - | Input(input/textarea) |
| touchstart(o) | opts | - | Touch start |
| touchmove(o) | opts | - | Touch move |
| touchend(o) | opts | - | Touch end |
| trigger(t,d) | type,detail | - | Trigger event |
| callMethod(m,...) | method,args | - | Call component method |
| data(path) | path(opt) | any | Component render data |
| setData(d) | data | - | Set component data |
| callContextMethod(m,...) | method,args | - | video context |
| scrollWidth | - | number | scroll-view width |
| scrollHeight | - | number | scroll-view height |
| scrollTo(x,y) | x,y | - | scroll-view scroll |
| swipeTo(i) | index | - | swiper slide |
| moveTo(x,y) | x,y | - | movable-view move |
| slideTo(v) | value | - | slider slide |

## CSS Selector Support

Only supports a subset of WXSS selectors:
- `.class` `#id` `element` `element,element`
- `::after` `::before`
- Does NOT support: descendant selectors, child selectors, attribute selectors

Elements within custom components must be searched via `element.$()` within the component scope.