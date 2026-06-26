# memegen.link API Reference

Base URL: `https://api.memegen.link`

## URL Structure

```
https://api.memegen.link/images/{template}/{top_text}/{bottom_text}.{format}
```

## Formats

| Extension | Description |
|-----------|-------------|
| `.jpg` | Smaller files |
| `.png` | Higher quality |
| `.gif` | Animated (if template supports it, or animates text on static backgrounds) |
| `.webp` | Animated (same as gif) |

## Special Characters in URLs

| Input | URL Encoding | Notes |
|-------|-------------|-------|
| Space | `_` (underscore) | Most common |
| Space | `-` (dash) | Alternative |
| Literal `_` | `__` (double underscore) | |
| Literal `-` | `--` (double dash) | |
| Newline | `~n` | Multi-line text |
| `?` | `~q` | |
| `&` | `~a` | |
| `%` | `~p` | |
| `#` | `~h` | |
| `/` | `~s` | |
| `\` | `~b` | |
| `<` | `~l` | |
| `"` | `''` (two single quotes) | |
| Emojis | Direct characters or `:alias:` | e.g., 👍 or `:thumbsup:` |

## Empty Lines

Use `_` for an empty/blank text line: `/images/template/_/bottom_text.jpg`

## Query Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `width` | int | Scale to specific width |
| `height` | int | Scale to specific height |
| `layout` | string | `top` for top-only text positioning |
| `font` | string | Font id (see below) |
| `style` | string | Template style variant or image URL overlay |
| `color` | string | Text color as HTML name or hex code |
| `background` | URL | Custom background image (use with `custom` template) |

## Fonts

| Name | ID | Alias |
|------|------|-------|
| Titillium Web Black | `titilliumweb` | `thick` |
| Kalam Regular | `kalam` | `comic` |
| Impact | `impact` | — |
| Noto Sans Bold | `notosans` | — |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/templates` | List all available templates (JSON array) |
| GET | `/templates/{id}` | Get template details |
| GET | `/images/{id}/{top}/{bottom}.{ext}` | Generate meme image |
| GET | `/fonts` | List available fonts |

## Verified Working Templates

| ID | Name | Lines | Best For |
|----|------|-------|----------|
| `drake` | Drakeposting | 2 | Two contrasting options |
| `fry` | Futurama Fry | 2 | Skepticism / not sure |
| `rollsafe` | Roll Safe | 2 | Clever life hacks |
| `spongebob` | Mocking SpongeBob | 2 | Sarcasm / mockery |
| `buzz` | X, X Everywhere | 2 | Something is everywhere |
| `pigeon` | Is This a Pigeon? | 3 | Misidentifying things |
| `pooh` | Tuxedo Winnie the Pooh | 2 | Classy vs basic |
| `db` | Distracted Boyfriend | 3 | Three-way comparison |
| `slap` | Will Smith Slap | 2 | Getting hit by something |
| `woman-cat` | Woman Yelling at Cat | 2 | Argument / overreaction |
| `kermit` | But That's None of My Business | 2 | Passive aggression |
| `harold` | Hide the Pain Harold | 2 | Hidden suffering |
| `fine` | This is Fine | 2 | Everything on fire |
| `success` | Success Kid | 2 | Small victories |
| `morpheus` | Matrix Morpheus | 2 | What if I told you |
| `stonks` | Stonks | 2 | Financial / going up |
| `khaby-lame` | Khaby Lame Shrug | 2 | Obvious solutions |
| `kombucha` | Kombucha Girl | 2 | Trying something weird |
| `gru` | Gru's Plan | 4 | Plan backfires |
| `chair` | American Chopper Argument | 6 | Escalating argument |
| `astronaut` | Always Has Been | 4 | Revelation / "always" |
| `same` | They're The Same Picture | 3 | Things that are identical |
| `right` | Anakin Padmé | 5 | "Right?" repetition |
| `glasses` | Peter Parker's Glasses | 2 | Before/after clarity |
| `gb` | Galaxy Brain | 4 | Escalating intelligence |
| `cmm` | Change My Mind | 1 | Hot takes |
| `wonka` | Condescending Wonka | 2 | Condescension |
| `spiderman` | Spider-Man Pointing | 2 | Things that are the same |
| `handshake` | Epic Handshake | 3 | Agreement / common ground |
| `reveal` | Scooby Doo Reveal | 4 | Unmasking something |
| `doge` | Doge | 2 | Much wow |
| `inigo` | Inigo Montoya | 2 | You keep using that word |
| `philosoraptor` | Philosoraptor | 2 | Deep questions |
| `keanu` | Conspiracy Keanu | 2 | Wild conspiracy theories |
| `custom` | Custom background | varies | Use `?background=URL` |

## ⚠️ Broken Templates (avoid)

| ID | Issue |
|----|-------|
| `simply` | Grey striped background, no image |
| `always` | Grey striped background (use `astronaut` or Imgflip URL instead) |
| `panik` | 3-panel doesn't render properly |

For the full template list: `GET https://api.memegen.link/templates`
