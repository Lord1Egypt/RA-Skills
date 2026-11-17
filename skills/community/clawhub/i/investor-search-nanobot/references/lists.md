# Lists

Every list `SKILL.md` refers to. **One entry per quoted token.** Entries may contain spaces
(`"s r o"`, `"sdn bhd"`) — split on the quotes, never on whitespace.

> A tester transcribing an earlier `·`-separated version split it on whitespace, injected
> the single letters `a`, `s`, `p`, `o` as suffixes, and mangled every name it touched
> (`Nadira` → `nadir`). That is why this file exists and why everything here is quoted.

**Extending these is normal work.** A market whose forms are missing produces silent
duplicates — not an error, just a wrong file. Before working a market not covered below,
look up its company forms and add them — to `investor-search/lists-local.md` in the
workspace, tagged with the market, never to this file: an installed skill that has been
edited stops receiving skill updates (`SKILL.md`, *nanobot*).

---

## 1. Legal forms — stripped from BOTH ENDS, repeatedly, in fold step 5

Match each however written: `s.r.o.` · `s r o` · `sro` · `S.R.O.` are one entry.

**⚠ Strip from BOTH ends.** Baltic and Nordic registries put the form in front — `AS Vesta`
against the firm's own `Vesta`, while the same register writes `Vesta Capital AS`. An
end-anchored strip folds one and not the other, and no list entry can fix an anchor.

```
Germany / Austria / Switzerland
"gmbh" "mbh" "ag" "kg" "co kg" "gmbh co kg" "ug" "ohg" "gbr" "ev" "se" "kgaa"
"stiftung" "genossenschaft" "eg"

Czechia / Slovakia
"a s" "s r o" "spol s r o" "k s" "v o s" "z s" "o p s" "druzstvo"

Poland
"sp z o o" "s a" "sp k" "sp j" "sp komandytowa" "sp z oo sp k"

United Kingdom / Ireland / United States / Canada
"ltd" "limited" "private limited" "llp" "lp" "llc" "l l c" "inc" "incorporated"
"corp" "corporation" "plc" "co" "company" "pc" "pllc" "ulc" "cic"

France / Belgium / Luxembourg / Monaco
"sas" "sasu" "sarl" "s a r l" "sa" "scs" "sca" "snc" "sci" "sam" "scsp"

Netherlands
"bv" "b v" "nv" "n v" "cv" "vof" "coop"

Italy / Spain / Portugal
"spa" "s p a" "srl" "s r l" "sl" "s l" "slu" "sapa" "lda" "sgps" "scr" "sicar"

Nordics / Baltics
"ab" "publ" "oy" "oyj" "asa" "aps" "hf" "ehf" "ou" "oü" "as" "uab" "sia" "ab lt"
"mtü" "tü" "ky" "ks" "ans" "da"
Estonia  "ou" "osauhing" "as" "aktsiaselts" "tu" "taisuhing" "uu" "usaldusuhing"
         "tuh" "tulundusuhistu" "mtu" "mittetulundusuhing" "sa" "sihtasutus" "fie"
Latvia   "sia" "as" "ik" "ps" "ks" "vsia"
Lithuania "uab" "ab" "mb" "tub" "kub" "vsi" "ii"

Gulf / MENA
"fze" "fzco" "fz llc" "llc fz" "fzc" "dmcc" "pjsc" "pssc" "psc" "jsc" "est"
"establishment" "wll" "w l l" "sal" "spc" "sao" "saog" "saoc" "cscc"

Asia-Pacific
"pte" "pte ltd" "pte limited" "sdn bhd" "bhd" "berhad" "pty" "pty ltd" "kk"
"gk" "yk" "kabushiki kaisha" "vcc" "lvcc" "opc" "ltda" "tbk" "pt"

Latin America
"sa de cv" "sapi de cv" "sab de cv" "srl de cv" "eirl" "spa" "ltda"

Fund and trust vehicles
"sicav" "sicaf" "fcp" "raif" "scsp" "gp" "lp" "llp" "trust" "foundation"
"fund" "fund i" "fund ii" "master fund" "feeder fund"
```

**⚠ `"private limited"` and `"pte ltd"` spelled out.** Missing them splits
`X Capital Private Limited` from `X Capital` — and spelled-out `Private Limited` is
Singapore's commonest written form.

**⚠ `"vcc"` — Singapore's Variable Capital Company.** The standard fund vehicle there.

**⚠ Jurisdictions are NOT legal forms.** Never strip these — they distinguish real firms:

```
"difc" "adgm" "ifsc" "gift city" "qfc" "aifc" "labuan"
```

---

## 2. Generic tails — stripped in fold step 8, only if what remains is distinctive

```
"family office" "family offices" "investment office" "private office" "wealth office"
"investment group" "investment" "investments" "invest" "investing" "capital"
"ventures" "venture" "partners" "partnership" "holding" "holdings" "group"
"groups" "gruppe" "skupina" "grupa" "grupo" "groupe" "beteiligungen"
"beteiligungsgesellschaft" "vermögensverwaltung" "asset management" "management"
"conglomerate" "enterprises" "industries" "vc" "pe" "fo" "mfo" "sfo"
```

`Vesta Ventures` and `Vesta VC` are one firm. `ventures` was on this list and `vc` was not.

## 3. Region words — fold step 7, before the distinctiveness test

Without this, `Aldebaran Capital` and `Aldebaran Capital Asia` never reach the test at all,
because the tail strip is end-anchored and `asia` is not a generic tail.

```
"asia" "asia pacific" "apac" "europe" "european" "emea" "mena" "gcc" "nordic"
"nordics" "iberia" "benelux" "latam" "americas" "international" "global"
"worldwide" "overseas"
```

---

## 4. Place words — a token on this list is NEVER distinctive

**This list is a starting point, not a closed set.** It cannot enumerate the world.

**The operative rule is in `SKILL.md`: if you cannot decide whether a token is a place,
treat it as a place and do not fold.** Refusing to fold costs a flag; folding costs the
truth. `Raffles` is a person, a district and a hotel brand — and five unrelated Singapore
organisations key to it.

```
countries and regions   every country name and demonym, plus:
                        "asia" "europe" "mena" "gulf" "levant" "balkan" "baltic"
                        "alpine" "nordic" "iberian" "adriatic"

Gulf                    "dubai" "abu dhabi" "sharjah" "ajman" "fujairah"
                        "ras al khaimah" "umm al quwain" "doha" "riyadh" "jeddah"
                        "manama" "kuwait" "muscat" "emirates"

Europe                  "london" "paris" "munich" "münchen" "hamburg" "frankfurt"
                        "berlin" "zurich" "zürich" "geneva" "vienna" "wien"
                        "prague" "praha" "brno" "warsaw" "kraków" "milan" "madrid"
                        "amsterdam" "stockholm" "copenhagen" "bavaria" "bayern"
                        "tyrol" "moravia" "silesia"

Asia-Pacific            "singapore" "hong kong" "tokyo" "seoul" "shanghai"
                        "beijing" "shenzhen" "mumbai" "delhi" "bangalore"
                        "jakarta" "kuala lumpur" "sydney" "melbourne"
                        "far east" "orchard" "marina" "raffles"

Americas                "new york" "boston" "chicago" "dallas" "miami"
                        "san francisco" "silicon valley" "toronto" "vancouver"
                        "são paulo" "mexico city" "bogotá" "buenos aires"
```

---

## 5. Investor-type words — Job 4's allowlist

**Every word in a candidate string must be owned by the type it claims.** An allowlist, not
a denylist: a denylist of qualifiers is unbounded, and the next unlisted one gets stored as
something else in silence.

```
family_office      "family" "families" "office" "offices" "single" "multi" "private"
                   "familienbüro" "familienunternehmen" "rodinná" "rodinný"
                   "kancelář" "bureau" "familial" "oficina" "familiar" "ufficio"
                   "famiglia" "familiare"

investment_group   "investment" "investments" "invest" "invests" "investing" "group"
                   "groups" "holding" "holdings" "skupina" "grupa" "gruppe"
                   "investiční" "beteiligungsgesellschaft" "conglomerate"
                   "enterprises"

private_equity     "private" "equity" "buyout" "buyouts" "pe" "growth" "capital"
                   "mezzanine" "secondaries" "secondary" "credit" "debt" "direct"
                   "lending" "special" "situations" "distressed" "infrastructure"
                   "real" "estate" "assets" "timber" "farmland" "managers"
                   "management" "manager"

venture_capital    "vc" "vcs" "venture" "ventures" "capital" "fund" "funds" "firm"
                   "firms" "investor" "investors" "seed" "early" "stage"

angel              "angel" "angels" "investor" "investors" "business" "syndicate"
                   "network" "club"

unknown            "unknown" "unclassified" "unset" "none" "tbd" "n a"
```

**A strategy is not an entity type.** Mezzanine, secondaries, private credit, timber, real
estate and infrastructure describe *what a fund does*, not *what kind of organisation it is*
— so those words are owned by `private_equity` above, and the strategy itself belongs in
**`sectors`**, never in `type`. Without this, 10 of 29 rows in one small market shipped as
`unknown` for firms whose business was perfectly clear.

**Include every morphological form or a firm cannot be typed from its own sentence.** An
earlier version had `investment` and `investments` but not `invest`, so a firm founded
*"to **invest** in potential business ideas"* was untypeable from its own words; `private`
was owned by nothing, so *"The Private Office of …"* — one of the commonest family-office
name forms in Dubai — could not be typed at all. **Check this whenever you add a market.**

### Names that signal a type — narrower, and only when no page states one

```
family office · familienbüro · familienunternehmen · rodinná kancelář  → family_office
ventures · venture capital · standalone "VC"                          → venture_capital
```

`Capital` · `Invest` · `Holding` · `Group` · `Gruppe` · `AG` · `GmbH` resolve to
**nothing**. Measured on a production corpus: resolves 27 of 106 `unknown` firms, leaves 79
alone. **That rate is European and does not transfer** — outside it, prefer `unknown`.

---

## 6. People — titles and suffixes

```
leading titles     "dr" "prof" "professor" "mr" "mrs" "ms" "mx" "herr" "frau"
                   "sir" "dame" "dipl" "ing" "mag" "ir" "drs" "eng"

trailing suffixes  "jr" "sr" "ii" "iii" "iv" "phd" "mba" "msc" "bsc" "ma" "ba"
                   "cfa" "cpa" "cfp" "caia" "frm" "md" "esq" "llm" "jd" "acca"
```

Both are stripped **repeatedly** — *"X, CFA, PhD"* carries two and one pass strips one.
