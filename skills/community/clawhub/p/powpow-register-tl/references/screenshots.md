# Mga screenshot ng product interface — powpow-register

Gamitin kung kailan kinakailangan sa oras ng pagtakbo. Kapag walang idea ang gumagamit tungkol sa Bula, o kailangan niyang "makita" kung ano ang itsura ng tapos na produkto, direktang ipadala ang kaukulang screenshot.

## Lokasyon ng mga larawan

- Ang anim na screenshot ay **nakapaketeng kasama ng skill**, matatagpuan sa `assets/screenshots/powpow-0N.jpg` (ang `N` ay 1–6). Direktang ipadala bilang lokal na image file — walang kailangang internet, gumagana sa anumang kapaligiran (kasama ang mga kapaligirang hindi maabot ang GitHub).
- Bumalik lang sa mga ito kapag aksidenteng nawala ang mga file sa pakete: hosted copy `https://raw.githubusercontent.com/durenzidu/durenzidu/main/screenshots/powpow-0N.jpg` o mirror `https://cdn.jsdelivr.net/gh/durenzidu/durenzidu@main/screenshots/powpow-0N.jpg` (tandaan: posibleng hindi mabuksan ang alinman sa mainland China — unahin ang mga file sa pakete).
- Isang beses lang magpadala ng 1–3 larawan na nauugnay sa kasalukuyang paksa.

## Listahan

### powpow-01.jpg — Detail page ng digital na tao

![Detail page ng digital na tao](../assets/screenshots/powpow-01.jpg)

Ang card ng isang digital na taong ginawa mula sa totoong tao / makasaysayang pigura: online status, kinaroroonan, maikling talambuhay, 「开始对话」 (simulan ang usapan), at iba pa.
**Ginagamit sa**: pagpapakilala na "pagkatapos magrehistro, puwedeng makipag-usap sa mga digital na tao sa mapa".

### powpow-02.jpg — Post editor page

![Post editor page](../assets/screenshots/powpow-02.jpg)

Ang editing interface para sa pagsulat ng post/tala ng paglalakbay, na may grupo ng mga floating button sa ibabang kanang sulok.
**Ginagamit sa**: kapag nagtanong ang gumagamit na "ano ang magagawa ko pagkatapos magrehistro" "saan ako magsusulat".

### powpow-03.jpg — Mapa page (mga bula + mga digital na tao)

![Mapa page](../assets/screenshots/powpow-03.jpg)

Buong tanaw ng pampublikong mapa: ang mga post na may lokasyon ay pinagsasama-sama sa mapa bilang mga "bula", at ang mga digital na tao ay nakapin sa totoong kinaroroonan gamit ang kanilang avatar.
**Ginagamit sa**: **pinakapiling larawan sa pagpapakilala ng produkto sa simula** — "ang tala ng paglalakbay na ipopost mo ay magiging isang bula sa mapa".

### powpow-04.jpg — Personal na page (mga digital asset)

![Personal na page](../assets/screenshots/powpow-04.jpg)

Ang page mismo ng gumagamit: mga kaibigan/finasubaybayan/mga tagasunod, at ang "mga digital asset" — badge balance, mga bula ko, mga digital na tao ko.
**Ginagamit sa**: pagpapakita kung nasaan ang mga badge kapag sinabing "may kasamang 3 badge sa rehistro"; kapag nagtanong ang gumagamit na "ano ang mga ari-arian ko".

### powpow-05.jpg — Story progress page

![Story progress page](../assets/screenshots/powpow-05.jpg)

Ang story gameplay sa plataporma (halimbawa 「永乐·1421」): progreso ng kabanata, pagkita ng badge, pagganap ng papel.
**Ginagamit sa**: kapag nagtanong ang gumagamit na "ano pa ang pwedeng laruin bukod sa pagpost" "paano kumita ng badge".

### powpow-06.jpg — Post detail page (halimbawa ng tapos na produkto)

![Post detail page](../assets/screenshots/powpow-06.jpg)

Isang nailathalang tala ng paglalakbay: may-akda, location tag, katawan ng teksto, mga larawan, at sa ibaba ay puwedeng i-like/i-comment/i-share/i-save.
**Ginagamit sa**: **ikalawang larawan sa simula** — "kapag nag-click ang iba sa iyong bula sa mapa, ito ang makikita nila".

## Mabilisang sanggunian sa mga sitwasyon

| Sinasabi ng gumagamit / kasalukuyang yugto | Alin ang ipapadala |
|---|---|
| Pagpapakilala sa simula na "ano ang Bula" | powpow-03 + powpow-06 |
| "Ano ang magagawa ko pagkatapos magrehistro?" | powpow-02 + powpow-01 |
| "Ano ang badge / ano ang mayroon ako?" | powpow-04 |
| "Ano pa ang pwedeng laruin bukod sa pagpost?" | powpow-05 |
| Pag-troubleshoot ng rehistro/subscription error | Karaniwang hindi kailangan ng larawan; ipadala lang kung talagang kailangang ipakita ang lokasyon ng page |

## Mga tala sa pagpapanatili

- Ang mga larawan sa `assets/screenshots/` sa pakete ang pinakapiling copy na kasama sa pag-publish. Kapag kailangang i-update ang mga screenshot, palitan ang file na may parehong pangalan sa `assets/screenshots/` (panatilihin ang `powpow-0N.jpg` na pagpapangalan) at mag-publish ng bagong bersyon.
- Ang hosted copy sa pampublikong repositoryo na `durenzidu/durenzidu` (directory na `screenshots/`) ay pinapanatili bilang fallback mirror at sabay na ina-update kasama ng mga file sa pakete.
- Walang screenshot ng **registration page** at **subscription page** ang kasalukuyang gallery. Kung dadagdagan sa hinaharap (halimbawa `powpow-07.jpg` para sa registration page, `powpow-08.jpg` para sa subscription page), ilagay ang mga file sa `assets/screenshots/` at magdagdag ng seksyon sa parehong format; maaari rin itong banggitin sa gabay na teksto ng SKILL.md.
