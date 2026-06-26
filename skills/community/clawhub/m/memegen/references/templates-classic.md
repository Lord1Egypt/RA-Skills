# Classic Meme Templates — Hardcoded Fallback

When the Imgflip API is unreachable, use these stable image URLs with the memegen.link `custom` template:

```
https://api.memegen.link/images/custom/{top}/{bottom}.png?background={template_url}&width=800
```

Remember to URL-encode the background URL:

```python
from urllib.parse import quote
bg = quote("https://i.imgflip.com/30b1gx.jpg", safe=":/")
url = f"https://api.memegen.link/images/custom/top/bottom.png?background={bg}&width=800"
```

## Top 30 Templates

| # | Name | Imgflip ID | Image URL |
|---|------|-----------|-----------|
| 1 | Drake Hotline Bling | 181913649 | `https://i.imgflip.com/30b1gx.jpg` |
| 2 | Two Buttons | 87743020 | `https://i.imgflip.com/1g8my4.jpg` |
| 3 | Distracted Boyfriend | 112126428 | `https://i.imgflip.com/1ur9b0.jpg` |
| 4 | Change My Mind | 129242436 | `https://i.imgflip.com/24y43o.jpg` |
| 5 | UNO Draw 25 Cards | 217743513 | `https://i.imgflip.com/3lmzyx.jpg` |
| 6 | Bernie Asking | 222403160 | `https://i.imgflip.com/3oevdk.jpg` |
| 7 | Woman Yelling At Cat | 188390779 | `https://i.imgflip.com/345v97.jpg` |
| 8 | Expanding Brain | 93895088 | `https://i.imgflip.com/1jwhww.jpg` |
| 9 | Batman Slapping Robin | 438680 | `https://i.imgflip.com/9ehk.jpg` |
| 10 | One Does Not Simply | 61579 | `https://i.imgflip.com/1bij.jpg` |
| 11 | Tuxedo Winnie Pooh | 178591752 | `https://i.imgflip.com/2ybua0.jpg` |
| 12 | Epic Handshake | 135256802 | `https://i.imgflip.com/28j0te.jpg` |
| 13 | Waiting Skeleton | 4087833 | `https://i.imgflip.com/2fm6x.jpg` |
| 14 | Futurama Fry | 61520 | `https://i.imgflip.com/1bgw.jpg` |
| 15 | Hide the Pain Harold | 27813981 | `https://i.imgflip.com/gk5el.jpg` |
| 16 | Always Has Been | 252600902 | `https://i.imgflip.com/46e43q.png` |
| 17 | Monkey Puppet | 161865971 | `https://i.imgflip.com/2gnnjh.jpg` |
| 18 | Megamind Peeking | 370867422 | `https://i.imgflip.com/64sz4u.png` |
| 19 | Laughing Leo | 259237855 | `https://i.imgflip.com/4acd7j.png` |
| 20 | Panik Kalm Panik | 226297822 | `https://i.imgflip.com/3qqcim.png` |
| 21 | Is This A Pigeon | 100777631 | `https://i.imgflip.com/1o00in.jpg` |
| 22 | Buff Doge vs Cheems | 247375501 | `https://i.imgflip.com/43a45p.jpg` |
| 23 | Left Exit 12 Off Ramp | 124822590 | `https://i.imgflip.com/22bdq6.jpg` |
| 24 | Think Mark Think | 316466202 | `https://i.imgflip.com/58wkde.jpg` |
| 25 | Same Picture | 180190441 | `https://i.imgflip.com/2za3u1.jpg` |
| 26 | Mocking Spongebob | 102156234 | `https://i.imgflip.com/1otk96.jpg` |
| 27 | Running Away Balloon | 131087935 | `https://i.imgflip.com/261o3j.jpg` |
| 28 | Blank Nut Button | 119139145 | `https://i.imgflip.com/1yxkcp.jpg` |
| 29 | X All The Y | 91538330 | `https://i.imgflip.com/1ihzfe.jpg` |
| 30 | Ancient Aliens | 101470 | `https://i.imgflip.com/26am.jpg` |

## As Python Dict (copy-paste ready)

```python
CLASSIC_TEMPLATES = [
    {"id": "181913649", "name": "Drake Hotline Bling", "url": "https://i.imgflip.com/30b1gx.jpg"},
    {"id": "87743020", "name": "Two Buttons", "url": "https://i.imgflip.com/1g8my4.jpg"},
    {"id": "112126428", "name": "Distracted Boyfriend", "url": "https://i.imgflip.com/1ur9b0.jpg"},
    {"id": "129242436", "name": "Change My Mind", "url": "https://i.imgflip.com/24y43o.jpg"},
    {"id": "217743513", "name": "UNO Draw 25 Cards", "url": "https://i.imgflip.com/3lmzyx.jpg"},
    {"id": "222403160", "name": "Bernie Asking", "url": "https://i.imgflip.com/3oevdk.jpg"},
    {"id": "188390779", "name": "Woman Yelling At Cat", "url": "https://i.imgflip.com/345v97.jpg"},
    {"id": "93895088", "name": "Expanding Brain", "url": "https://i.imgflip.com/1jwhww.jpg"},
    {"id": "438680", "name": "Batman Slapping Robin", "url": "https://i.imgflip.com/9ehk.jpg"},
    {"id": "61579", "name": "One Does Not Simply", "url": "https://i.imgflip.com/1bij.jpg"},
    {"id": "178591752", "name": "Tuxedo Winnie Pooh", "url": "https://i.imgflip.com/2ybua0.jpg"},
    {"id": "135256802", "name": "Epic Handshake", "url": "https://i.imgflip.com/28j0te.jpg"},
    {"id": "4087833", "name": "Waiting Skeleton", "url": "https://i.imgflip.com/2fm6x.jpg"},
    {"id": "61520", "name": "Futurama Fry", "url": "https://i.imgflip.com/1bgw.jpg"},
    {"id": "27813981", "name": "Hide the Pain Harold", "url": "https://i.imgflip.com/gk5el.jpg"},
    {"id": "252600902", "name": "Always Has Been", "url": "https://i.imgflip.com/46e43q.png"},
    {"id": "161865971", "name": "Monkey Puppet", "url": "https://i.imgflip.com/2gnnjh.jpg"},
    {"id": "370867422", "name": "Megamind Peeking", "url": "https://i.imgflip.com/64sz4u.png"},
    {"id": "259237855", "name": "Laughing Leo", "url": "https://i.imgflip.com/4acd7j.png"},
    {"id": "226297822", "name": "Panik Kalm Panik", "url": "https://i.imgflip.com/3qqcim.png"},
    {"id": "100777631", "name": "Is This A Pigeon", "url": "https://i.imgflip.com/1o00in.jpg"},
    {"id": "247375501", "name": "Buff Doge vs Cheems", "url": "https://i.imgflip.com/43a45p.jpg"},
    {"id": "124822590", "name": "Left Exit 12 Off Ramp", "url": "https://i.imgflip.com/22bdq6.jpg"},
    {"id": "316466202", "name": "Think Mark Think", "url": "https://i.imgflip.com/58wkde.jpg"},
    {"id": "180190441", "name": "Same Picture", "url": "https://i.imgflip.com/2za3u1.jpg"},
    {"id": "102156234", "name": "Mocking Spongebob", "url": "https://i.imgflip.com/1otk96.jpg"},
    {"id": "131087935", "name": "Running Away Balloon", "url": "https://i.imgflip.com/261o3j.jpg"},
    {"id": "119139145", "name": "Blank Nut Button", "url": "https://i.imgflip.com/1yxkcp.jpg"},
    {"id": "91538330", "name": "X All The Y", "url": "https://i.imgflip.com/1ihzfe.jpg"},
    {"id": "101470", "name": "Ancient Aliens", "url": "https://i.imgflip.com/26am.jpg"},
]
```
