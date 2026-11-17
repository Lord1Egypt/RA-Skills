# Travel Handdrawn Map Visual Workflow

Use this playbook when the user wants a Xiaohongshu travel map, food map,
city-walk map, local-life route map, handdrawn itinerary, or illustrated
check-in order image.

Trigger phrases:

- 旅游手绘地图
- 美食地图
- 旅行地图
- 城市地图
- city walk 地图
- 打卡路线图
- 一天从早吃到晚
- 5 天游路线
- 帮我做一张像手绘攻略一样的图
- 把这些店 / 景点 / 路线做成地图

## Core Judgment

This is not a normal poster.

It is a saveable route image. The value comes from:

- city / destination anchor
- route order
- food or attraction anchors
- recognizable local landmarks
- cute handdrawn texture
- practical itinerary box
- one-second title recognition

If the user only says "做一张某地旅游地图" with no route, places, food,
duration, or target audience, do not generate immediately. Ask for the minimum
route data first.

## Minimum Intake

Ask only the fields that change the map.

Use this compact intake:

> 你把这 5 个信息发我就能做：
> 1. 城市/目的地：
> 2. 地图主题：美食 / 景点 / city walk / 亲子 / 情侣 / 省钱 / 5 天游？
> 3. 你想放几个点：5 个、6 个还是 8 个？
> 4. 每个点的名字和一句话说明：
> 5. 有没有参考图或想要配色？

If the user has no place list, offer a low-cost path:

> 如果你还没整理地点，我可以先按你的城市和主题给你做一个“待确认版结构”，但具体店名/景点最好你确认后再生成，避免地图看起来好看但不好用。

If the user has a Xiaohongshu note/link or screenshot, first choose the safe
intake path:

- For screenshots or pasted route details, extract the visible details directly.
- For Xiaohongshu links, do not open the link before scope confirmation. First
  route through `research-scope-guard.md` and ask whether to make one online
  lookup to read the public note, or ask the user to paste the route details
  instead.

After the user confirms the online lookup or provides visible details, extract:

- city / area
- route order
- places / dishes / landmarks
- title promise
- visual density
- whether it is food-first or route-first

Then adapt it into the user's own map. Do not copy exact creator text, logo,
private characters, or route if the user does not have the right to use it.

## Default Map Types

### 1. Food Route Map

Use for city food, snacks, old streets, store hopping, local-life accounts, and
"从早吃到晚" topics.

Required elements:

- large title: city + food map
- subtitle: one-day / half-day / night snack / local old street promise
- 5-8 numbered route pins
- 4-7 illustrated dishes or drinks
- small storefront / street / landmark drawings
- right-side or bottom "打卡顺序" box
- saveable line such as "辣度量力而行", "少排队多留白", "本地人路线"

Best for:

- 长沙美食地图
- 南宁老友粉路线
- 汕头牛肉火锅地图
- 上海老店小吃路线
- 夜宵路线 / 打工人平价吃法

### 2. Travel Itinerary Map

Use for province/city travel, 2-5 day routes, ancient towns, mountains, rivers,
parks, museums, and weekend plans.

Required elements:

- large title: destination + travel map
- subtitle: duration + theme, such as "山水古镇 5 天游"
- simplified destination silhouette or soft terrain shape
- 5-8 numbered pins
- arrows or a winding route line
- illustrated landmarks, nature, bridge, old town, waterfall, mountain, river
- side route suggestion: D1, D2, D3...
- travel objects: suitcase, camera, signpost, bus, boat, ticket, compass

Best for:

- 贵州旅游地图
- 云南 5 天游路线
- 广西山水路线
- 上海 city walk
- 周末亲子路线

### 3. City-Walk Neighborhood Map

Use for a smaller district, old street, neighborhood, museum route, coffee shop
route, photo route, bookstore route, or "walkable day".

Required elements:

- district / neighborhood name
- walking route line
- 3-6 places
- time blocks, such as morning / afternoon / evening
- small street scenes, signs, storefronts, coffee, books, park, river
- one practical note: "少赶路", "适合拍照", "雨天也能走"

## Visual Style

Use a warm handdrawn travel-journal style:

- vertical Xiaohongshu image, default 3:4 or 4:5
- cream / parchment / watercolor paper background
- black brush-calligraphy title or thick hand-lettering
- red underline under the title
- watercolor route line, usually brown or red-brown
- numbered red map pins
- cute local character or mascot at corners when appropriate
- hearts, stars, arrows, dotted boxes, signposts, small labels
- food and landmarks should look appetizing/recognizable, not photorealistic
- keep Chinese text short, high-contrast, and readable

Do not use:

- realistic satellite map
- generic flat vector map with no warmth
- clean corporate infographic style
- too many tiny unreadable labels
- fake exact geography when the user did not provide route order
- store names, prices, or addresses that the user did not provide

## Content Structure

Before image generation, produce a structured map brief:

1. **Map title**
2. **Subtitle**
3. **Route points table**
   - number
   - place
   - food / attraction
   - one short label
   - illustration subject
4. **Route order box**
5. **Bottom slogan**
6. **Visual prompt**
7. **Xiaohongshu caption**
8. **10 publishing keywords**

For food maps, use this point table:

| No. | Place | Food | Label | Illustration |
| --- | --- | --- | --- | --- |
| 1 | street/store/area | dish | one short reason | dish + storefront |

For travel maps, use this point table:

| Day/No. | Place | Why go | Label | Illustration |
| --- | --- | --- | --- | --- |
| D1/1 | attraction/area | one short reason | route label | landmark/nature |

## Prompt Requirements

The image-generation prompt must include:

- "handdrawn watercolor illustrated travel map"
- exact city / destination
- exact title and subtitle
- aspect ratio: vertical 3:4 or 4:5
- cream textured paper background
- black Chinese brush-calligraphy title
- numbered route pins
- winding route line or simplified region silhouette
- illustrated local foods / landmarks
- side itinerary box or route-order box
- cute sticker accents
- readable Chinese labels only
- no logos, no real brand marks, no QR code, no fake exact address

When text rendering is unreliable, reduce text:

- title
- subtitle
- 5-6 point names
- route-order box
- bottom slogan

Put longer captions in the Xiaohongshu body copy instead of the image.

## Quality Gate

Before returning the map, check:

- Can the user tell the city and theme in 1 second?
- Are the route points numbered clearly?
- Is there a save reason: itinerary, food order, map, budget, or route?
- Are the food/landmark illustrations connected to the theme?
- Is the right-side or bottom route-order box readable?
- Is the map cute but still useful?
- Are there hallucinated stores, addresses, prices, or claims?
- If geography may be inaccurate, did you label it as an illustrated route map
  rather than an exact navigation map?

## User-Facing Follow-Up

End with one practical next step:

- 你把城市和 5 个地点发我，我直接给你做成一张手绘路线图。
- 如果你没有地点，我先给你做一个可替换地点的版式，等你确认店名/景点后再生成最终版。
- 发出去后把链接和后台截图给我，我帮你看收藏率和评论区是不是在问路线/店名/价格。
