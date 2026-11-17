#!/usr/bin/env python3
"""Generate prompts/*.md from scene specs. Run from repo root."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "prompts"

PREFIX = (
    "Photoreal vertical UGC photo, 9:16, shot on a recent iPhone, handheld. "
    "Real skin texture, visible pores, flyaway hair, no beauty filter. "
)
SUFFIX = (
    " Natural color, slight noise, no ring light unless it belongs in this room. "
    "No on-screen text, no caption, no watermark, no sticker, no extra fingers, "
    "no warped packaging, no invented logos."
)

UNBOXING_INTRO = """# Unboxing openings (U-01 to U-25)

Each scene has a **still prompt** (first frame) and a **Seedance 2.5 prompt** (image-to-video). Fill `[PRODUCT]`, `[PACKAGING]`, `[CREATOR]`. Generate the still at 9:16, then run Seedance 2.5: first frame = still, **8s**, **720×1280**, audio on. Draft at 480×854.

The still is the first frame: package in hand, product not fully revealed. See `docs/seedance-2.5.md`.
"""

STREET_INTRO = """# Street interview openings (S-01 to S-25)

Each scene has a **still prompt** and a **Seedance 2.5 prompt**. Fill `[PRODUCT]`, `[CREATOR]` (the interviewee). Still at 9:16, then Seedance 2.5 I2V: 8s, 720×1280, audio on.

The still is the interviewer's phone: subject mid-reaction, product in someone's hands.
"""

FACE_INTRO = """# Face-cam review openings (F-01 to F-25)

Each scene has a **still prompt** and a **Seedance 2.5 prompt**. Fill `[PRODUCT]`, `[CREATOR]`. Still at 9:16, front camera. Then Seedance 2.5 I2V: 8s, 720×1280, audio on.
"""

QA_INTRO = """# Q&A / who sells more openings (Q-01 to Q-25)

Each scene has a **still prompt** and a **Seedance 2.5 prompt**. Fill `[PRODUCT]` and two people inside `[CREATOR]` (example: `two friends, late 20s, one in a baseball cap`). Still at 9:16, then Seedance 2.5 I2V: 8s, 720×1280, audio on.
"""

I2V_TAIL = (
    "Light: keep the existing lighting and composition.\n\n"
    "No subtitles. No on-screen text. No watermark. One continuous take, no cuts. "
    "[PRODUCT] is rigid. It does not melt or change label. Five fingers on each hand.\n\n"
    "**Seedance 2.5:** duration `8` · `720×1280` · draft `480×854` · audio on · first frame = the still."
)


def infer_audio(body: str, fmt: str) -> str:
    s = body.lower()
    if any(k in s for k in ("kitchen", "island", "counter", "fridge", "sink", "dish")):
        return "tape or cardboard, a short breath, fridge hum, mug on laminate. No BGM, only ambient and action sounds."
    if any(k in s for k in ("car", "passenger", "driver", "windshield", "parking")):
        return "cabin rattle, distant traffic, seat fabric, a short breath. No BGM, only ambient and action sounds."
    if any(k in s for k in ("street", "sidewalk", "subway", "bus ", "mall", "campus", "park", "boardwalk")):
        return "outdoor ambience, faint voices or traffic, product tap in the hands. No BGM, only ambient and action sounds."
    if any(k in s for k in ("bathroom", "vanity", "shower", "mirror")):
        return "small-room echo, plastic or glass tap, close voice. No BGM, only ambient and action sounds."
    if any(k in s for k in ("gym", "locker")):
        return "locker-room hum, zipper, bottle or box tap. No BGM, only ambient and action sounds."
    if any(k in s for k in ("cafe", "bookstore", "latte")):
        return "cafe murmur, cup on saucer, paper rustle. No BGM, only ambient and action sounds."
    if any(k in s for k in ("office", "desk", "cubicle", "laptop")):
        return "HVAC, keyboard leftover, package rustle. No BGM, only ambient and action sounds."
    if fmt == "unboxing":
        return "tape or cardboard, a short breath, room tone of this room. No BGM, only ambient and action sounds."
    if fmt == "street":
        return "street ambience, faint traffic, their short reply. No BGM, only ambient and action sounds."
    if fmt == "face":
        return "close-mic voice, room tone of this room, one product handling sound. No BGM, only ambient and action sounds."
    return "two overlapping voices, room tone, a product tap. No BGM, only ambient and action sounds."


def i2v_prompt(fmt: str, hook: str, body: str) -> str:
    audio = infer_audio(body, fmt)
    said = f'They look at the lens and say: "{hook}".'
    if fmt == "unboxing":
        shot = (
            "An 8-second vertical UGC clip, 9:16.\n\n"
            "Shot: handheld phone, chest height over the package, organic micro-shake, no dolly, no orbit, no cinematic grade.\n\n"
            "Subject: keep the person, room, wardrobe, [PACKAGING], and [PRODUCT] identical to the first frame. Do not redesign the label.\n\n"
            "Action:\n"
            "[0-2s]: hands settle on [PACKAGING], eyes flick to the lens, mouth already moving.\n"
            "[2-6s]: open the package the real way — peel tape, lift a flap, or pop a lid. Do not skip to a clean hero. [PRODUCT] stays inside until this window.\n"
            f"[6-8s]: lift [PRODUCT] into the lower third, turn it once in the same light. {said}\n\n"
            f"Audio: {audio}"
        )
    elif fmt == "street":
        shot = (
            "An 8-second vertical UGC clip, 9:16.\n\n"
            "Shot: handheld interviewer phone, arm's length, slight wide-angle distortion, organic micro-shake, no gimbal smoothness, no cinematic grade.\n\n"
            "Subject: keep both people, the street, wardrobe, and [PRODUCT] identical to the first frame. Do not add crew or new bystanders.\n\n"
            "Action:\n"
            "[0-2s]: interviewee finishes hearing the question, eyes go from interviewer to [PRODUCT].\n"
            f"[2-6s]: they turn [PRODUCT], feel the weight, or bring it closer to read. Background pedestrians drift, they do not teleport. {said}\n"
            "[6-8s]: a real laugh, grimace, or shrug, then they lift [PRODUCT] a little toward the lens.\n\n"
            f"Audio: {audio}"
        )
    elif fmt == "face":
        shot = (
            "An 8-second vertical UGC clip, 9:16, front camera.\n\n"
            "Shot: handheld front camera, selfie-arm fatigue (tiny drift), no switch to a rear camera, no gimbal, no cinematic grade.\n\n"
            "Subject: keep the same face, hair, wardrobe, room, and [PRODUCT] as the first frame. Do not apply a beauty filter over time.\n\n"
            "Action:\n"
            "[0-2s]: talking to the lens, natural blinks, small head movement. The hand with [PRODUCT] gestures once.\n"
            f"[2-6s]: bring [PRODUCT] closer or do one real use (pump, shake, uncap, unfold). Face stays in frame. {said}\n"
            "[6-8s]: settle back, finish the thought, same energy as the still.\n\n"
            f"Audio: {audio}"
        )
    else:
        shot = (
            "An 8-second vertical UGC clip, 9:16.\n\n"
            "Shot: handheld phone capturing both people, slight wide, organic micro-shake, no split screen, no vs graphic, no cinematic grade.\n\n"
            "Subject: keep both people, the room, wardrobe, and the single [PRODUCT] identical to the first frame. Do not clone the product.\n\n"
            "Action:\n"
            "[0-2s]: the asker is already finishing the question. The other person starts to answer.\n"
            f"[2-6s]: they talk over each other a little. [PRODUCT] gets pointed at, passed, or tapped. One head-shake, one lean-in. {said}\n"
            "[6-8s]: both glance at the lens as if they remembered the camera, then a laugh or an argument face.\n\n"
            f"Audio: {audio}"
        )
    return shot + "\n\n" + I2V_TAIL


def block(sid: str, title: str, hook: str, body: str, fmt: str) -> str:
    still = PREFIX + body.strip() + SUFFIX
    return (
        f"## {sid} — {title}\n\n"
        f"**Hook line (caption later):** {hook}\n\n"
        f"**Still prompt:**\n\n{still}\n\n"
        f"**Seedance 2.5 prompt** (I2V, first frame = the still):\n\n{i2v_prompt(fmt, hook, body)}\n"
    )


def write(
    name: str,
    intro: str,
    scenes: list[tuple[str, str, str, str]],
    fmt: str,
) -> None:
    parts = [intro, ""]
    for sid, title, hook, body in scenes:
        parts.append(block(sid, title, hook, body, fmt))
    (OUT / name).write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {name} ({len(scenes)} scenes)")


UNBOXING = [
    (
        "U-01",
        "Kitchen island, morning mail",
        "I wasn't even going to film this",
        "[CREATOR] at a cramped apartment kitchen island in hard morning window light. "
        "A stack of junk mail and a stained coffee mug sit left. Both hands peel packing tape on [PACKAGING]. "
        "[PRODUCT] is still inside, only a corner visible. Eyes flick up to the lens, mid-sentence. "
        "Cheap laminate counter, dish rack behind.",
    ),
    (
        "U-02",
        "Bedroom floor, cross-legged",
        "okay wait this packaging is extra",
        "[CREATOR] sits cross-legged on a rumpled duvet, afternoon sidelight from a cheap blind. "
        "[PACKAGING] in the lap, thumbs under the flap. Phone is on a pillow, slightly low angle. "
        "Laundry pile at the foot of the bed. [PRODUCT] not out yet.",
    ),
    (
        "U-03",
        "Couch, TV mute",
        "I sat down for one second",
        "[CREATOR] on a sagging couch, TV glow on the wall, show paused. "
        "[PACKAGING] on knees, one socked foot visible. Remote and a half-eaten snack on the cushion. "
        "Overhead warm lamp. Looking at the camera like a roommate just walked in.",
    ),
    (
        "U-04",
        "Parked car, passenger seat",
        "I opened it in the parking lot",
        "[CREATOR] in a passenger seat, seatbelt off, daylight through a dirty windshield. "
        "[PACKAGING] on the thighs, tearing the strip. Cup holder with a gas-station drink. "
        "Phone held by a hand on the headrest or dashboard. [PRODUCT] still boxed.",
    ),
    (
        "U-05",
        "Bathroom counter, skincare clutter",
        "this was not on my list",
        "[CREATOR] at a messy bathroom vanity, mirror lights uneven, toothpaste tube uncapped. "
        "Hands on [PACKAGING] among other bottles. [PRODUCT] peeking from tissue paper. "
        "Front-camera-ish angle from the phone leaning on a toothbrush cup. Condensation on the mirror.",
    ),
    (
        "U-06",
        "Office desk after lunch",
        "my lunch break unboxing",
        "[CREATOR] at a generic office desk, ID lanyard, sad salad container open. "
        "Overhead fluorescent plus monitor glow. [PACKAGING] in the keyboard well, scissors in one hand. "
        "Cubicle felt or a laptop sticker visible. Eyes to camera, slightly guilty.",
    ),
    (
        "U-07",
        "Apartment stoop",
        "it just got dropped off",
        "[CREATOR] sitting on concrete stoop steps, overcast daylight, building door behind. "
        "Amazon-style pile of other boxes. Hands ripping [PACKAGING]. Neighborhood street out of focus. "
        "Jacket still on. [PRODUCT] not revealed.",
    ),
    (
        "U-08",
        "Cafe table, couldn't wait",
        "I could not wait until I got home",
        "[CREATOR] at a small cafe table by the window, latte art already dead. "
        "[PACKAGING] next to the saucer, pulling tissue. Other customers blurred. "
        "Phone on the table edge, slightly wide. Rain or city on the glass.",
    ),
    (
        "U-09",
        "Gym bag on locker bench",
        "this came with me to the gym for some reason",
        "[CREATOR] on a locker-room bench, damp hair, duffel open. Fluorescent lights. "
        "[PACKAGING] on the bench slats, opening it between sets of shoes. "
        "Phone propped on the bag. [PRODUCT] still wrapped.",
    ),
    (
        "U-10",
        "Hotel bed, travel",
        "hotel unboxing because I have no self control",
        "[CREATOR] on a hotel duvet, blackout curtain cracked, ugly art on the wall. "
        "[PACKAGING] on the white sheets, tearing the seal. Mini fridge and a kettle in the background. "
        "Phone on a room-service tray. Tired, smiling anyway.",
    ),
    (
        "U-11",
        "Kitchen sink, wet hands",
        "I didn't even dry my hands",
        "[CREATOR] at a crowded sink, wet hands leaving prints on [PACKAGING]. "
        "Window over the sink, dishes in the rack. Phone on the drying mat. "
        "Hair clipped up. [PRODUCT] still inside a wet mailer.",
    ),
    (
        "U-12",
        "Closet floor, clothes haul",
        "I sat on the floor like a child",
        "[CREATOR] on closet carpet, hangers and shoes around. Overhead closet bulb, yellowish. "
        "[PACKAGING] between the knees. Phone on a shoe box. Looking up at the lens.",
    ),
    (
        "U-13",
        "Dining table, roommate watching",
        "they're judging me and I don't care",
        "[CREATOR] at a scuffed dining table, second person blurred in a doorway watching. "
        "Evening indoor light. [PACKAGING] in the center, tape half off. "
        "Phone at table height. A takeout bag still on the table.",
    ),
    (
        "U-14",
        "Nightstand, late delivery",
        "this dinged at 11pm",
        "[CREATOR] in bed, phone flashlight plus a dim lamp. [PACKAGING] on the nightstand, sitting up to open it. "
        "Charging cables, water glass, alarm clock. Face puffy, hair messy. [PRODUCT] still boxed.",
    ),
    (
        "U-15",
        "Park picnic table",
        "I walked it to the park",
        "[CREATOR] at a weathered picnic table, trees behind, overcast. "
        "[PACKAGING] on the wood slats, pigeons or a bike in the background. "
        "Jacket sleeves pushed up. Phone on a water bottle. [PRODUCT] not out.",
    ),
    (
        "U-16",
        "Laundry room folding table",
        "opened it on the dryer like a gremlin",
        "[CREATOR] in a tight laundry room, washer humming implied, overhead bulb. "
        "[PACKAGING] on the dryer lid, ripping the bag. Basket of unfolded clothes. "
        "Phone leaning on detergent. Slightly sweaty, no makeup required.",
    ),
    (
        "U-17",
        "Garage workbench",
        "this is not a garage product but here we are",
        "[CREATOR] at a cluttered workbench, fluorescent shop light, tools out of focus. "
        "[PACKAGING] among screws and a shop rag. Hands dusty. Phone on a vice. "
        "Garage door half open, daylight spilling in.",
    ),
    (
        "U-18",
        "Kids' playroom, adult unboxing",
        "I said I'd wait until they napped",
        "[CREATOR] on a playroom rug among toys, kid out of frame or a closed door. "
        "Soft daylight. [PACKAGING] in the lap. Phone on a toy bin. Whispering energy, finger near lips almost.",
    ),
    (
        "U-19",
        "Makeup vanity, golden hour",
        "I cleared one square of this table",
        "[CREATOR] at a crowded makeup desk, sunset through a window, palettes stacked. "
        "Hands lifting tissue from [PACKAGING]. Phone in a mini tripod among brushes. "
        "[PRODUCT] still mostly hidden. Real skin, no facetune.",
    ),
    (
        "U-20",
        "Fridge door open",
        "I put the box in the kitchen and then I lost it",
        "[CREATOR] holding the fridge door with an elbow, [PACKAGING] on the counter beside condiments. "
        "Fridge light plus kitchen overhead. Phone on the counter. Looking at camera, annoyed-amused.",
    ),
    (
        "U-21",
        "Window seat, plants",
        "this is my one nice corner",
        "[CREATOR] on a window seat with tired houseplants, late afternoon. "
        "[PACKAGING] on folded legs. Phone on a stacked book. Soft but not cinematic light. "
        "City or backyard through the glass, a bit dirty.",
    ),
    (
        "U-22",
        "Hallway, keys still in hand",
        "I didn't even put my keys down",
        "[CREATOR] in a narrow apartment hallway, shoes half off, keys hanging from a finger. "
        "Other hand tearing [PACKAGING] against the wall. Entry light. Phone on the shoe cabinet. "
        "Mail slot or coats in frame.",
    ),
    (
        "U-23",
        "Airport lounge",
        "layover unboxing, do not recommend, did it anyway",
        "[CREATOR] in a generic airport seat, carry-on at the feet, fluorescent concourse. "
        "[PACKAGING] on the lap, trying to open quietly. Phone at chest height. "
        "Other travelers blurred. [PRODUCT] still packed.",
    ),
    (
        "U-24",
        "Backyard patio",
        "opened it outside because the tape was loud",
        "[CREATOR] at a cheap patio table, string lights unlit, daylight. "
        "[PACKAGING] on the plastic table, neighbor fence behind. Phone against a plant pot. "
        "Slight wind in hair. Cardboard bits on the table.",
    ),
    (
        "U-25",
        "Bookstore cafe",
        "I was supposed to be reading",
        "[CREATOR] at a bookstore cafe table, paperbacks stacked, overheard chatter implied. "
        "[PACKAGING] beside a pastry plate, sliding a finger under the flap. "
        "Phone next to a bookmark. Warm indoor light, not styled.",
    ),
]

STREET = [
    (
        "S-01",
        "Downtown sidewalk, lunch rush",
        "would you try this if a stranger handed it to you",
        "Interviewer's arm-length phone, slight wide-angle. [CREATOR] on a crowded downtown sidewalk at lunch, tote bag, one earbud in. "
        "Holding [PRODUCT], squinting at the label. Storefronts and pedestrians out of focus. Overcast daylight, hard pavement shadow.",
    ),
    (
        "S-02",
        "Campus quad",
        "be honest you're a student would you buy this",
        "[CREATOR] on a campus path with a backpack, mid-laugh, holding [PRODUCT] at chest height. "
        "Brick building behind, bikes. Interviewer hand visible at frame edge. Midday sun.",
    ),
    (
        "S-03",
        "Farmers market aisle",
        "you just bought produce, now this",
        "[CREATOR] between produce stalls, canvas bag of greens, turning [PRODUCT] in both hands. "
        "Tent canopy light, other shoppers. Phone from interviewer, slightly low.",
    ),
    (
        "S-04",
        "Mall corridor",
        "would you stop for this in a mall",
        "[CREATOR] in a bright mall hallway, shopping bags, skeptical look at [PRODUCT]. "
        "Storefront lights mixed with daylight from a skylight. Tile floor glare. Interviewer phone.",
    ),
    (
        "S-05",
        "Subway entrance stairs",
        "you have 20 seconds, thoughts",
        "[CREATOR] on subway stairs, city daylight above, holding [PRODUCT] while half-turned to leave. "
        "Commuters blurred. Interviewer's phone from two steps down. Wind.",
    ),
    (
        "S-06",
        "Coffee shop patio",
        "you already have a coffee, do you still care",
        "[CREATOR] at a metal cafe table on the sidewalk, paper cup, leaning back, [PRODUCT] in one hand. "
        "Passerby. Interviewer sitting across, phone at table height. Soft overcast.",
    ),
    (
        "S-07",
        "Park path, dog owner",
        "if I wasn't holding a leash maybe",
        "[CREATOR] on a park path, dog leash in one hand, [PRODUCT] in the other, amused. "
        "Trees, a trash can, another walker. Interviewer phone, slightly shaky crop.",
    ),
    (
        "S-08",
        "Night market / food stall glow",
        "this is a weird place to pitch me",
        "[CREATOR] under warm stall lights at dusk, holding [PRODUCT] next to a paper food tray. "
        "Neon or string lights bokeh. Interviewer phone. Grease-shine on fingers is fine.",
    ),
    (
        "S-09",
        "Office plaza, smokers' corner",
        "we have four minutes, go",
        "[CREATOR] in work clothes on a plaza bench, badge on a lanyard, [PRODUCT] resting on a knee. "
        "Glass building behind. Mid-afternoon. Interviewer standing, phone down at them.",
    ),
    (
        "S-10",
        "Flea market",
        "you're already buying random stuff, what about this",
        "[CREATOR] among folding tables of junk, holding [PRODUCT] compared to something else in the other hand. "
        "Harsh sun, tarps. Interviewer phone. Dust in the air.",
    ),
    (
        "S-11",
        "Gym parking lot",
        "pre-workout opinions only",
        "[CREATOR] in gym clothes beside a car, gym bag strap, unscrewing or holding [PRODUCT]. "
        "Asphalt, other cars. Late day sun. Interviewer phone across the open car door.",
    ),
    (
        "S-12",
        "Bus stop",
        "if the bus comes I'm leaving mid-sentence",
        "[CREATOR] at a bus shelter, phone in one hand, [PRODUCT] in the other, looking down the street then at the lens. "
        "Ads on the shelter out of focus. Overcast. Interviewer just off-frame.",
    ),
    (
        "S-13",
        "Bookstore sidewalk",
        "you read, does this feel like a scam",
        "[CREATOR] outside a bookstore, tote with books, examining [PRODUCT] like a blurb. "
        "Daylight, bike rack. Interviewer phone. Mild side-eye.",
    ),
    (
        "S-14",
        "Beach boardwalk",
        "sunscreen hands, be nice",
        "[CREATOR] on a boardwalk, wind, sunglasses on the head, holding [PRODUCT] away from the sun to read it. "
        "Railing, ocean smear in background. Interviewer phone, bright, a bit overexposed like a real phone.",
    ),
    (
        "S-15",
        "Grocery exit",
        "you just spent money, one more thing",
        "[CREATOR] outside a grocery, cart or bags, [PRODUCT] handed to them, weighing it. "
        "Automatic doors, circulars. Daylight. Interviewer phone. Tired face.",
    ),
    (
        "S-16",
        "University library steps",
        "study break, roast this",
        "[CREATOR] on library steps with a laptop sleeve, deadpan look at [PRODUCT]. "
        "Columns or brick. Overcast. Interviewer sitting one step below, phone up.",
    ),
    (
        "S-17",
        "Night downtown, after dinner",
        "would you buy this after two drinks",
        "[CREATOR] on a nighttime sidewalk, restaurant lights, slightly flushed, holding [PRODUCT] under a streetlamp. "
        "Interviewer's phone with mixed tungsten and LED. Friends blurred behind.",
    ),
    (
        "S-18",
        "Skate park rail",
        "no corporate answers",
        "[CREATOR] sitting on a skate park ledge, board nearby, turning [PRODUCT]. "
        "Concrete, afternoon sun, other skaters far. Interviewer phone, low.",
    ),
    (
        "S-19",
        "Thrift store dressing area",
        "you already like cheap, try this",
        "[CREATOR] near thrift racks, fluorescent, holding [PRODUCT] against a jacket on a hanger. "
        "Crowded aisle. Interviewer phone. Honest confusion on the face.",
    ),
    (
        "S-20",
        "Gas station pumps",
        "you have 90 seconds while this fills",
        "[CREATOR] at a pump, car door open, [PRODUCT] in hand, squinting. "
        "Canopy light, oil stains. Interviewer across the island, phone. Wind.",
    ),
    (
        "S-21",
        "Dog park fence",
        "talk to me not the dogs",
        "[CREATOR] leaning on a chain-link fence, [PRODUCT] resting on the rail, watching dogs then the camera. "
        "Late afternoon. Interviewer phone. Grass and dirt.",
    ),
    (
        "S-22",
        "Train platform",
        "if your train's here, just yell the answer",
        "[CREATOR] on a platform, backpack, [PRODUCT] at chest, LED signs blurred. "
        "Overcast or underground fluorescents. Interviewer phone. Coat on.",
    ),
    (
        "S-23",
        "High school pickup line (adults)",
        "parent to parent, no pitching",
        "[CREATOR] as an adult in a school pickup line, car keys, [PRODUCT] on the window ledge. "
        "Daylight, other cars. Interviewer between bumpers, phone. Honest, not cute.",
    ),
    (
        "S-24",
        "Hardware store parking",
        "you came for screws",
        "[CREATOR] in a hardware apron-adjacent parking lot, paper bag of parts, inspecting [PRODUCT] like a tool. "
        "Sun, orange carts far away. Interviewer phone.",
    ),
    (
        "S-25",
        "Rainy awning",
        "we're both stuck here anyway",
        "[CREATOR] under a shop awning in light rain, damp hair, holding [PRODUCT] close to the chest. "
        "Wet sidewalk reflections. Interviewer phone. Breath in cold air if it fits.",
    ),
]

FACE = [
    (
        "F-01",
        "Bathroom mirror, morning",
        "don't come at me before coffee",
        "Front camera, [CREATOR] in a bathroom, mirror behind showing the phone. Uneven vanity lights. "
        "[PRODUCT] in the other hand near the chin. Mid-sentence, mouth open. Toothbrush in the sink. Real skin.",
    ),
    (
        "F-02",
        "Parked car, seatbelt on",
        "I had to say this before I went inside",
        "Front camera in a parked car, [CREATOR] in the driver's seat, seatbelt, daylight on one side of the face. "
        "[PRODUCT] on the steering wheel or passenger seat, one hand lifting it. Soft window dirt bokeh.",
    ),
    (
        "F-03",
        "Bedroom ceiling, lying down",
        "I have been thinking about this for an hour",
        "Front camera held above the face, [CREATOR] lying on a pillow, messy hair, ceiling fan or popcorn ceiling. "
        "[PRODUCT] resting on the chest. Nightstand lamp. Quiet, close.",
    ),
    (
        "F-04",
        "Kitchen, cooking pause",
        "I ruined dinner to tell you this",
        "Front camera, [CREATOR] at a stove or cutting board, slightly shiny from cooking, [PRODUCT] in the non-knife hand. "
        "Steam or a pan in the background. Overhead kitchen light.",
    ),
    (
        "F-05",
        "Desk job, headphones off",
        "my manager is going to see this and I don't care",
        "Front camera at a laptop desk, [CREATOR] with headset around the neck, [PRODUCT] beside the trackpad, picking it up. "
        "Monitor glow. Sticky notes. Deadpan.",
    ),
    (
        "F-06",
        "Walk-and-talk sidewalk",
        "keep walking with me",
        "Front camera, [CREATOR] walking a residential sidewalk, bounce in the frame, [PRODUCT] swinging in the other hand then raised. "
        "Overcast. Houses, a mailbox. Wind on the mic implied by hair.",
    ),
    (
        "F-07",
        "Closet, getting dressed",
        "I almost wore the other thing",
        "Front camera, [CREATOR] in a closet, half-dressed in a normal way, [PRODUCT] held next to an outfit on a hanger. "
        "Warm closet bulb. Clothes on the floor.",
    ),
    (
        "F-08",
        "Couch under a blanket",
        "this is a blanket review",
        "Front camera, [CREATOR] under a throw on the couch, TV light, [PRODUCT] peeking from the blanket. "
        "Tired eyes. Living room mess.",
    ),
    (
        "F-09",
        "Gym mirror selfie angle",
        "I look insane and that's fine",
        "Front camera in a gym mirror area, [CREATOR] flushed, [PRODUCT] at chest, water bottle. "
        "Fluorescents, machines behind. Not a flex pose, a talk.",
    ),
    (
        "F-10",
        "Grocery aisle whisper",
        "I'm whispering because this is feral",
        "Front camera low in a grocery aisle, [CREATOR] whispering, [PRODUCT] next to a shelf item they were comparing. "
        "Harsh store light. Cart handle in frame.",
    ),
    (
        "F-11",
        "Bathroom after shower",
        "I am still in a towel, deal with it",
        "Front camera, [CREATOR] in a towel or robe, fogged mirror, [PRODUCT] in hand. "
        "Damp hair, real skin. Phone a little wet-looking at the edges of the frame is fine.",
    ),
    (
        "F-12",
        "Fire escape or balcony",
        "I came outside so I wouldn't yell",
        "Front camera on a small balcony, city or alley behind, [CREATOR] in a hoodie, [PRODUCT] on the railing then picked up. "
        "Daylight, a plant dying in a pot.",
    ),
    (
        "F-13",
        "Makeup wipe, end of day",
        "this is the leftover-makeup version of me",
        "Front camera at a vanity, [CREATOR] with makeup half removed, cotton pad, [PRODUCT] in the other hand. "
        "Warm lamp. Honest face.",
    ),
    (
        "F-14",
        "Laundromat",
        "I have 32 minutes on this dryer",
        "Front camera, [CREATOR] in a laundromat chair, [PRODUCT] on a magazine table, machines behind. "
        "Fluorescent, slightly green. Bored then engaged.",
    ),
    (
        "F-15",
        "Kid asleep, hallway whisper",
        "if I wake them I will cry",
        "Front camera in a dim hallway, [CREATOR] whispering, [PRODUCT] held close, finger near lips. "
        "Night-light spill. Real parent energy, no baby in frame unless necessary.",
    ),
    (
        "F-16",
        "Office bathroom stall-adjacent (sink)",
        "work bathroom, no shame",
        "Front camera at a workplace restroom sink, tile, paper towels, [CREATOR] holding [PRODUCT] like a secret. "
        "Fluorescent. Checking the door in the mirror.",
    ),
    (
        "F-17",
        "Sunset passenger window",
        "say it before we lose the light, not in a poetic way, the sun is just going down",
        "Front camera, [CREATOR] in the passenger seat, sunset hitting half the face, [PRODUCT] against the window then pulled in. "
        "Seatbelt. Unflattering and real.",
    ),
    (
        "F-18",
        "Standing fridge light",
        "I am eating leftovers and also this",
        "Front camera, fridge open lighting the face, [CREATOR] holding [PRODUCT] and a container. "
        "Kitchen dark behind. Funny, not styled.",
    ),
    (
        "F-19",
        "Rainy window, inside",
        "weather is doing too much, this is not",
        "Front camera, [CREATOR] at a rainy window, droplets, indoor tungsten, [PRODUCT] in the foreground. "
        "Sweater. Quiet talk.",
    ),
    (
        "F-20",
        "Hair-in-clips, getting ready",
        "clips in, opinions out",
        "Front camera, [CREATOR] with hair clips, [PRODUCT] near the face, bathroom or bedroom. "
        "Messy, mid-routine. One earring in.",
    ),
    (
        "F-21",
        "Over-ear headphones, commute",
        "I paused the podcast for this",
        "Front camera on public transit or a platform, [CREATOR] with headphones, [PRODUCT] lifted into frame. "
        "Mixed light, other passengers blurred. Indoor-outdoor mix.",
    ),
    (
        "F-22",
        "Pet in frame, unhelpful",
        "they are not going to help me explain this",
        "Front camera on a couch or floor, a cat or dog occupying space, [CREATOR] holding [PRODUCT] away from the pet. "
        "Living room daylight. Soft chaos.",
    ),
    (
        "F-23",
        "Golden hour kitchen, not cinematic on purpose",
        "the sun is annoying and also fine",
        "Front camera, [CREATOR] in a kitchen with a hot window behind, slight silhouette fight, [PRODUCT] catching the light. "
        "Squinting. Real, not a beer ad.",
    ),
    (
        "F-24",
        "Hotel bathroom, travel size chaos",
        "I brought seven things and I still bought this",
        "Front camera, tiny hotel bathroom, toiletries bag exploded, [CREATOR] holding [PRODUCT] next to travel minis. "
        "Harsh vanity bulbs.",
    ),
    (
        "F-25",
        "End of a long day, doorway",
        "I haven't sat down yet",
        "Front camera, [CREATOR] in an apartment doorway, shoes half off, keys, [PRODUCT] still in a pocket or mail pile, lifting it. "
        "Hall light. Exhausted honesty.",
    ),
]

QA = [
    (
        "Q-01",
        "Couch argument, one product",
        "who would you actually buy this from",
        "Two people on a couch, phone on a coffee table, [PRODUCT] between them on a knee. "
        "One leaning in, one squinting at the label. Evening lamp. Living room mess. Candid, both faces readable.",
    ),
    (
        "Q-02",
        "Sidewalk, friends after food",
        "creator page or the actual website",
        "Two friends on a nighttime sidewalk outside a restaurant, [PRODUCT] being passed. "
        "Streetlight. One pointing, one unconvinced. Interviewer-style phone, both in frame.",
    ),
    (
        "Q-03",
        "Kitchen island, couple",
        "would you trust the person on TikTok or the brand",
        "[CREATOR] as a couple at a kitchen island, [PRODUCT] on the cutting board area. "
        "One talking with hands, one arms crossed. Overhead light. Phone at island height.",
    ),
    (
        "Q-04",
        "Desk at work, coworkers",
        "would you expense this",
        "Two coworkers at a desk, monitors behind, [PRODUCT] by the keyboard. "
        "One spinning the chair, one deadpan. Fluorescent. Phone from a third coworker, close.",
    ),
    (
        "Q-05",
        "Car back seat, two friends",
        "who is selling this better, us or them",
        "Two people in a back seat, parked, [PRODUCT] between them. "
        "Window light. One showing the camera, one covering their face laughing. Phone from the front seat.",
    ),
    (
        "Q-06",
        "Dorm room floor",
        "roommate tax: who gets the link",
        "Two people on a dorm floor, posters, [PRODUCT] on a textbook. "
        "One excited, one broke-looking. Overhead dorm light. Phone on a mini fridge.",
    ),
    (
        "Q-07",
        "Thrift mirror, two outfits",
        "who would you take fashion advice from",
        "Two people in a thrift dressing area, [PRODUCT] in one hand, a hanger in the other. "
        "Fluorescent. Disagreement on faces. Phone in a third hand or propped.",
    ),
    (
        "Q-08",
        "Picnic blanket",
        "if we had $20 left, this or snacks",
        "Two people on a park blanket, [PRODUCT] in the grass between. "
        "Daylight. One reaching, one blocking. Phone from above, still 9:16, faces clear.",
    ),
    (
        "Q-09",
        "Gym stretch area",
        "trainer or random creator, who are you paying",
        "Two people on gym mats, [PRODUCT] on the floor between water bottles. "
        "Fluorescent. One stretching, one arguing. Phone on a bag.",
    ),
    (
        "Q-10",
        "Hair salon wait",
        "foil in, opinions out: who sells more",
        "Two people in a salon waiting area, [PRODUCT] on a magazine. "
        "One in a cape or clips. Daylight plus mirrors. Phone from a lap.",
    ),
    (
        "Q-11",
        "Grocery freezer door",
        "impulse buy or you walked in for this",
        "Two people at an open freezer door, [PRODUCT] vs a grocery item in the other hand. "
        "Cold fog, store light. One tempted, one judging. Phone from the cart.",
    ),
    (
        "Q-12",
        "Balcony, two drinks",
        "after one drink, whose link are you clicking",
        "Two people on a small balcony, [PRODUCT] on the railing. "
        "Dusk. One shrugging, one insistent. Phone from inside the doorway.",
    ),
    (
        "Q-13",
        "Bookstore cafe, two laptops",
        "would you buy it from a thread or a store",
        "Two people with laptops, [PRODUCT] between mugs. "
        "One turning the laptop, one looking at the physical product. Warm indoor light. Phone on a third book.",
    ),
    (
        "Q-14",
        "Bathroom doorway, getting ready",
        "who do you believe, the ad or your friend",
        "One person in the bathroom, one in the doorway, [PRODUCT] being shown through the door. "
        "Vanity lights vs hall light. Skeptical vs hyped. Phone from the doorway person.",
    ),
    (
        "Q-15",
        "Target run, cart",
        "off the shelf or off this video",
        "Two people at a cart in a big-box aisle, [PRODUCT] in the child seat of the cart. "
        "Store light. Pointing at shelf vs phone. Candid, a bit chaotic.",
    ),
    (
        "Q-16",
        "Siblings, childhood bedroom leftover",
        "mom would buy whose version",
        "Two adult siblings on a twin bed or floor, old posters, [PRODUCT] between them. "
        "Window light. Competitive faces. Phone on a dresser.",
    ),
    (
        "Q-17",
        "Bar patio, golden ugly light",
        "if a stranger DM'd you this vs a brand email",
        "Two people at a sticky patio table, [PRODUCT] next to empty glasses. "
        "String lights. One leaning in, one shaking head. Phone on the table, wide.",
    ),
    (
        "Q-18",
        "Studio apartment, one chair",
        "who deserves the commission, be mean",
        "Two people sharing a small apartment, one in the only chair, [PRODUCT] on a shipping box used as a table. "
        "Daylight. Playful fight. Phone on a monitor.",
    ),
    (
        "Q-19",
        "Parking garage stairwell",
        "echo answers only: whose store",
        "Two people in a concrete stairwell, [PRODUCT] being held up like evidence. "
        "Cool overhead light. One on a higher step. Phone from below. Gritty, real.",
    ),
    (
        "Q-20",
        "IKEA-style showroom cheat",
        "display or real apartment, who are you buying",
        "Two people sitting on a showroom bed they shouldn't be on, [PRODUCT] on the fake nightstand. "
        "Store daylight. Giggling vs serious. Phone from the aisle, slightly illegal energy.",
    ),
    (
        "Q-21",
        "Group chat energy, two on a call... no, two in person with phones",
        "whose message are you trusting",
        "Two people showing each other their phones and [PRODUCT] at the same time. "
        "Cafe or couch. Confusion. Third phone (ours) capturing both screens slightly, product still the hero.",
    ),
    (
        "Q-22",
        "Farmers market, two tote bags",
        "small brand table vs this link in bio",
        "Two people among stalls, [PRODUCT] compared to a paper bag of produce. "
        "Daylight, canopy. One local-loyal, one online-loyal. Interviewer phone.",
    ),
    (
        "Q-23",
        "Late-night kitchen, fridge hum",
        "2am, whose story are you buying from",
        "Two people in a dark kitchen, fridge light, [PRODUCT] on the counter. "
        "Pajamas. Intense whisper-argument. Phone on the microwave.",
    ),
    (
        "Q-24",
        "Bleachers or park bench",
        "would you buy it from the person next to you",
        "Two people on a bench, [PRODUCT] between them, sports field or playground behind, out of focus. "
        "Afternoon. One offering, one leaning away. Phone from a standing friend.",
    ),
    (
        "Q-25",
        "Elevator, two floors of debate",
        "answer before the doors open",
        "Two people in a cramped elevator, [PRODUCT] at chest height, mirrored wall showing the phone. "
        "Overhead elevator light. One talking fast, one hitting a button. Candid, slightly too close.",
    ),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    assert len(UNBOXING) == 25 and len(STREET) == 25 and len(FACE) == 25 and len(QA) == 25
    write("unboxing.md", UNBOXING_INTRO, UNBOXING, "unboxing")
    write("street-interview.md", STREET_INTRO, STREET, "street")
    write("face-cam-review.md", FACE_INTRO, FACE, "face")
    write("qa-who-sells-more.md", QA_INTRO, QA, "qa")


if __name__ == "__main__":
    main()
