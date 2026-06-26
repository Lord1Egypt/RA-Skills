# Playbooks — landmark-hotel

> CLI command sequences. Knowledge is for parameter mapping — never answer without executing.

---

## Playbook A: City Landmark

**Trigger:** "hotel near West Lake", "西湖附近酒店"

```bash
flyai search-poi --city-name "{city}" --keyword "{poi}"
flyai search-hotel --dest-name "{city}" --poi-name "{official_poi_name}" --sort distance_asc --check-in-date {in} --check-out-date {out}
```

**Output emphasis:** Verify POI → search by distance.

---

## Playbook B: Ancient Town

**Trigger:** "stay in Wuzhen", "住在乌镇"

```bash
flyai search-poi --city-name "{city}" --keyword "{town}"
flyai search-hotel --dest-name "{town}" --poi-name "{town}" --hotel-types "客栈" --sort distance_asc
```

**Output emphasis:** Inns inside the scenic area.

---

## Playbook C: Theme Park

**Trigger:** "Disney hotel", "迪士尼附近"

```bash
flyai search-poi --city-name "{city}" --keyword "{park}"
flyai search-hotel --dest-name "{city}" --poi-name "{park}" --sort distance_asc
```

**Output emphasis:** Flag official partner hotels.

---

## Playbook D: Nature Area

**Trigger:** "hotel near Zhangjiajie"

```bash
flyai search-poi --city-name "{city}" --keyword "{park}"
flyai search-hotel --dest-name "{city}" --poi-name "{park}" --sort distance_asc
# If <3 results → expand to city-wide
```

**Output emphasis:** Split: near park vs city center with drive time.

---

