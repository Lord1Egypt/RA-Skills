# HOI4 National Focus Tree Syntax Reference

## Table of Contents

1. [Top-Level Structure](#2-top-level-structure)
2. [focus_tree Fields](#3-focus_tree-fields)
3. [focus Node Complete Field Reference](#4-focus-node-complete-field-reference)
4. [Joint Focus Trees (joint_focus)](#5-joint-focus-trees)
5. [Shared Focus Trees (shared_focus)](#6-shared-focus-trees)
6. [German Inner Circle Mechanism](#7-german-inner-circle-mechanism)
7. [Effects](#8-effects)
8. [Triggers](#9-triggers)
9. [Variables and UI](#10-variables-and-ui)
10. [Common Pitfalls](#11-common-pitfalls)

---

## 1. File Locations

```
# Standard mod structure for national_focus files:
{mod_folder}/common/national_focus/
    generic.txt          # generic fallback focus tree
    usa.txt              # United States
    germany.txt          # Germany (with Inner Circle)
    soviet.txt           # Soviet Union
    nordic_shared.txt    # Nordic joint tree
    habsburg_joint.txt   # Austro-Hungarian joint tree
    congo_shared.txt     # Congo shared tree (Belgium/Congo)
    ... (73 countries total)
```

---

## 2. Top-Level Structure

```txt
focus_tree = {
    id = {tree_id}                    # tree identifier, e.g. "ger_focus", "nordic_shared_focus"
    country = {                       # AI weight allocation
        factor = 1
        modifier = {
            tag = {TAG} factor = 2
            OR = { tag = {TAG1} tag = {TAG2} } factor = 0
        }
    }
    default = yes|no                   # yes = load as generic fallback for all undefined countries
    reset_on_civilwar = yes|no          # yes = reset tree on civil war
    initial_show_position = { focus = {focus_id} }
    continuous_focus_position = { x = {n} y = {n} }
    search_filter_prios = { ... }

    # reference shared/joint focuses from other files
    shared_focus = {id}
    shared_focus = {id2}

    # local focus nodes
    focus = { ... }
    joint_focus = { ... }    # can mix focus and joint_focus in same tree
}
```

---

## 3. focus_tree Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique tree identifier |
| `country` | block | AI weight allocation |
| `default` | bool | Load as generic fallback tree |
| `reset_on_civilwar` | bool | Reset on civil war |
| `initial_show_position` | block | Initial viewport anchor `{ focus = id }` |
| `continuous_focus_position` | block | Persistent focus button coordinates `{ x = n y = n }` |
| `shared_focus` | id | Reference shared/joint focus from other files (repeatable) |
| `search_filter_prios` | block | Filter priority ordering |

---

## 4. focus Node Complete Field Reference

```txt
focus = {
    id = {id}                              # unique identifier
    icon = GFX_{name}                       # GFX resource name
    x = {n}                                 # column position
    y = {n}                                 # row position (relative to y=0 row)
    relative_position_id = {id}             # relative positioning anchor
    cost = {n}                              # days (actual = x7 days; Inner Circle uses @constants)

    # ===== Prerequisites =====
    prerequisite = { focus = {id} }          # prerequisite focus (repeatable)
    mutually_exclusive = { focus = {id} }   # mutual exclusion (repeatable)

    # ===== Conditional Offsets =====
    # Multiple offsets: first matching trigger determines displayed position
    offset = {
        x = {n}  y = {n}
        trigger = { has_focus_tree = {tree_id} }
    }
    offset = {
        x = {n}  y = {n}
        trigger = { has_completed_focus = {id} }
    }

    # ===== Conditions =====
    available = { {trigger} }                # availability condition
    bypass = { {trigger} }                   # auto-bypass condition
    allow_branch = { {trigger} }             # branch permission
    cancel_if_invalid = yes|no               # yes = cancel on invalid (default: yes)
    continue_if_invalid = yes|no             # yes = continue if invalid (default: no)
    available_if_capitulated = yes|no        # yes = usable after capitulation

    # ===== AI Behavior =====
    ai_will_do = {
        base = {n}                            # base weight (default: 0 -- MUST SET)
        modifier = { factor = {n} {trigger} }
        modifier = { factor = 0 is_historical_focus_on = yes }  # off in historical mode
    }

    # ===== Search Filters =====
    search_filters = {
        FOCUS_FILTER_POLITICAL
        FOCUS_FILTER_INDUSTRY
        FOCUS_FILTER_RESEARCH
        FOCUS_FILTER_MANPOWER
        FOCUS_FILTER_ARMY_XP
        FOCUS_FILTER_NAVY_XP
        FOCUS_FILTER_AIR_XP
        FOCUS_FILTER_ANNEXATION
        FOCUS_FILTER_STABILITY
        FOCUS_FILTER_WAR_SUPPORT
        FOCUS_FILTER_INNER_CIRCLE
        FOCUS_FILTER_TVF_AUTONOMY
        FOCUS_FILTER_HISTORICAL
        FOCUS_FILTER_BALANCE_OF_POWER
        FOCUS_FILTER_POLITICAL_CHARACTER
        FOCUS_FILTER_PROPAGANDA
    }

    # ===== Dynamic Icon =====
    dynamic = yes
    icon = { trigger = { {trigger} } value = GFX_{name} }
    icon = { trigger = { {trigger} } value = GFX_{name2} }

    # ===== Text Icon =====
    text_icon = {style}

    # ===== Effect Blocks =====
    select_effect = { {effect} }              # immediate on selection (prevents AI stalling)
    complete_tooltip = { {effect} }           # tooltip only (no effect)
    completion_reward = { {effect} }           # main reward (all members share)
    hidden_effect = { {effect} }               # hidden reward (no tooltip shown)

    # ===== joint_focus specific =====
    joint_trigger = { {trigger} }              # joint tree membership check
    completion_reward_joint_originator = { {effect} }  # originator extra reward
    completion_reward_joint_member = { {effect} }      # member extra reward
}
```

---

## 5. Joint Focus Trees (joint_focus)

### 5.1 Nordic Model (Equal Allied Nations)

```txt
focus_tree = {
    id = nordic_shared_focus

    joint_focus = {
        id = NORDIC_northern_command
        dynamic = yes
        text_icon = NORDIC_focus_style

        x = -6
        y = 1
        relative_position_id = NORDIC_form_joint_alliance

        joint_trigger = { NORDIC_basic_joint_trigger = yes }

        # three-part reward
        completion_reward = {
            air_experience = 25
            navy_experience = 25
            army_experience = 25
            add_command_power = 25
        }
        completion_reward_joint_originator = {
            add_ideas = { NORDIC_command_ns }
            add_political_power = 100
        }
        completion_reward_joint_member = {
            add_political_power = 50
        }
    }
}
```

### 5.2 Austro-Hungarian Model (Multi-Relationship + Global Variables)

Three relationship modes:

```txt
available = {
    custom_trigger_tooltip = {
        tooltip = HABSBURG_is_subject_puppeteer_faction_leader_or_member_trigger_tt
        OR = {
            # Mode 1: Danubian Federation (allied + faction leader)
            AND = {
                is_faction_leader = yes
                any_allied_country = { HABSBURG_is_a_habsburg_viable_nation = yes }
            }
            # Mode 1 alt: not faction leader but allied to HUN or AUS
            AND = {
                is_faction_leader = no
                OR = {
                    AND = { is_in_faction_with = HUN HUN = { is_faction_leader = yes } }
                    AND = { is_in_faction_with = AUS AUS = { is_faction_leader = yes } }
                }
            }
            # Mode 2: Master (HUN/AUS with subject)
            AND = {
                original_tag = HUN
                any_subject_country = { HABSBURG_is_a_habsburg_viable_nation = yes }
            }
            # Mode 3: Subject (subject of HUN/AUS)
            AND = {
                is_subject = yes
                OR = { is_subject_of = HUN is_subject_of = AUS }
            }
        }
        HABSBURG_is_a_habsburg_viable_nation = yes
    }
}
```

### 5.3 Originator Check (Austro-Hungarian)

```txt
available = {
    custom_trigger_tooltip = {
        tooltip = HABSBURG_is_originator_country
        tag = global.AH_originator_country       # global var stores current originator
    }
    any_other_country = {
        OR = { is_in_faction_with = ROOT is_subject_of = ROOT }
        HABSBURG_is_a_habsburg_viable_nation = yes
    }
    is_subject = no
}
```

### 5.4 Global Variable System (Austro-Hungarian Exclusive)

All member nations share a single global counter, with the originator executing actual changes:

```txt
# member sees preview only
completion_reward = {
    effect_tooltip = {
        custom_effect_tooltip = HABSBURG_modify_economy_ns_intro
        add_to_variable = {
            global.HABSBURG_economy_consumer_goods_factor = -0.1
            tooltip = consumer_goods_factor_tt
        }
    }
}

# originator executes actual change
completion_reward_joint_originator = {
    hidden_effect = {
        custom_effect_tooltip = HABSBURG_modify_economy_ns_intro
        add_to_variable = {
            global.HABSBURG_economy_consumer_goods_factor = -0.1
            tooltip = consumer_goods_factor_tt
        }
    }
}

# global variable namespaces
global.HABSBURG_economy_*          # economic global
global.HABSBURG_army_*             # army global
global.HABSBURG_cavalry_*          # cavalry global
global.HABSBURG_industry_*          # industry global
global.AH_originator_country        # current originator tag
```

### 5.5 Conditional Rewards (Ideology Fork)

```txt
completion_reward_joint_originator = {
    IF = {
        limit = {
            ROOT = { OR = { has_government = democratic has_government = communism } }
        }
        add_stability = 0.1
        add_popularity = { ideology = democratic popularity = 0.15 }
        hidden_effect = { add_to_variable = { global.HABSBURG_xxx = 0.15 } }
    }
    IF = {
        limit = {
            ROOT = { OR = { has_government = neutrality has_government = fascism } }
        }
        add_ideas = HABSBURG_an_imperium_restored
        set_cosmetic_tag = HUN_EMPIRE      # change country cosmetic name
        IF = {
            limit = { NOT = { any_country = { is_subject_of = ROOT } } }
            effect_tooltip = { add_ideas = HABSBURG_imperial_integration }
        }
    }
}
```

---

## 6. Shared Focus Trees (shared_focus)

### 6.1 Congo Model (Master-Subject)

Asymmetric sharing: one country actually executes, the other previews + unlocks:

```txt
shared_focus = {
    id = CONGO_expand_villages
    dynamic = yes
    available = { original_tag = COG }     # only available to Congo
    available_if_capitulated = yes

    completion_reward = {
        IF = {
            limit = { original_tag = COG }
            COG_vast_uncentralized_nation_modifier_level_down = yes
            every_state = {
                limit = {
                    is_owned_and_controlled_by = ROOT
                    OR = { state = 295 state = 538 state = 718 }
                }
                add_extra_state_shared_building_slots = 1
            }
        }
        ELSE_IF = {
            limit = { original_tag = BEL COG = { is_subject_of = BEL } }
            # Belgium sees a preview of what Congo will gain
            effect_tooltip = {
                COG = { every_state = { ... } }
            }
        }
        # unlock the same focus for the other country
        hidden_effect = {
            BEL = { unlock_national_focus = CONGO_expand_villages }
        }
    }
}
```

### 6.2 unlock_national_focus Mechanism

Core of "one country completes, other country also completes":

```txt
hidden_effect = {
    # Congo completes -> unlock for Belgium
    BEL = { unlock_national_focus = CONGO_xxx }
    # Belgium completes -> unlock for Congo
    COG = { unlock_national_focus = CONGO_xxx }
    # track completion count
    CONGO_one_more_focus_done = yes
    # force refresh dynamic modifiers
    force_update_dynamic_modifier = yes
}
```

### 6.3 Cross-Country Dynamic Modifier Sharing

```txt
# Congo modifies a variable inside Belgium's dynamic modifier
add_to_variable = {
    var = BEL.COG_belgian_congo_colonial_dynamic_modifier_research_speed_factor
    value = 0.03
    tooltip = research_speed_factor_tt
}

# syntax: OTHER_TAG.modifier_name.field_name
```

---

## 7. German Inner Circle Mechanism

### 7.1 Core Constants

```txt
@inner_circle_time_tier_1 = 20     # tier 1/2 = 20 days
@inner_circle_time_tier_2 = 20
@inner_circle_time_tier_3 = 40     # tier 3 = 40 days
@inner_circle_days_to_start_focus = 14    # event trigger delay
@inner_circle_random_days = 14            # random float
@inner_circle_cd_days = 90               # cooldown days
```

### 7.2 Inner Circle Focus Structure

```txt
focus = {
    id = GER_party_chancellor_bormann
    icon = GFX_focus_GER_party_chancellor_bormann
    prerequisite = { focus = GER_fuhrerprinzip }
    mutually_exclusive = { focus = GER_party_chancellor_hess }
    x = 2  y = 0
    relative_position_id = GER_party_chancellor_hess
    cost = @inner_circle_time_tier_1    # = 2 days

    available = {
        if = {
            limit = { is_ai = yes }
            hidden_trigger = {
                NOT = { has_country_flag = GER_bormann_was_ascended_flag }
            }
        }
        has_government = fascism
        NOT = { has_country_leader = { ruling_only = yes character = GER_martin_bormann } }
        has_country_flag = GER_inner_circle_event_pending_flag
        GER_inner_circle_is_ascension_cd_over = yes   # cooldown check macro
        if = {
            limit = { has_country_flag = GER_inner_circle_cd_flag }
            custom_trigger_tooltip = {
                tooltip = GER_inner_circle_cd_days_tt
                NOT = { has_country_flag = GER_inner_circle_cd_flag }
            }
        }
    }

    cancel_if_invalid = no
    continue_if_invalid = no

    # KEY: prevents AI from stalling
    select_effect = { set_country_flag = GER_bormann_ascension_flag }

    search_filters = {
        FOCUS_FILTER_INNER_CIRCLE
        FOCUS_FILTER_POLITICAL_CHARACTER
        FOCUS_FILTER_POLITICAL
    }

    completion_reward = {
        custom_effect_tooltip = {
            localization_key = GER_ascension_of_character_tt
            CHARACTER = GER_martin_bormann
        }
        show_ideas_tooltip = GER_bormann_secretary_to_the_fuhrer
        custom_effect_tooltip = {
            localization_key = GER_ascension_of_character_focus_tt
            CHARACTER = GER_martin_bormann
        }
        hidden_effect = {
            # trigger succession event
            country_event = {
                id = GER_inner_circle_hess.01
                days = @inner_circle_days_to_start_focus
                random_days = @inner_circle_random_days
            }
            clr_country_flag = GER_hess_ascension_flag
            # set cooldown
            GER_inner_circle_set_ascension_cd = yes
            # prevent AI from repeating (cleared after ~4 years)
            set_country_flag = {
                flag = GER_hess_was_ascended_flag
                days = 1500
                value = 1
            }
        }
    }
}
```

### 7.3 Inner Circle Macros (defined by events)

| Macro | Purpose |
|-------|---------|
| `GER_inner_circle_is_ascension_cd_over = yes` | Check if cooldown ended |
| `GER_inner_circle_set_ascension_cd = yes` | Set 90-day cooldown |
| `GER_inner_circle_event_pending_flag` | Event pending flag |
| `GER_inner_circle_cd_flag` | Cooldown active flag |
| `GER_inner_circle_cd_days_tt` | Cooldown tooltip key |

### 7.4 show_ideas_tooltip Preview Mechanism

```txt
# in completion_reward: shows advisor preview
show_ideas_tooltip = GER_bormann_secretary_to_the_fuhrer

# with custom localization
custom_effect_tooltip = {
    localization_key = GER_ascension_of_character_tt
    CHARACTER = GER_martin_bormann
}
```

---

## 8. Effects

### 8.1 Political and Points

```txt
add_political_power = 50
add_command_power = 25
add_stability = 0.1
add_war_support = 0.1
add_popularity = { ideology = {type} popularity = {n} }
add_ideas = {idea}
remove_idea = {idea}
swap_country_leader_traits = { remove = {trait} add = {trait} }
```

### 8.2 Experience

```txt
army_experience = 25
navy_experience = 25
air_experience = 25
add_doctrine_cost_reduction = {
    name = {name}
    cost_reduction = 0.5
    uses = 1
    category = land_doctrine
}
```

### 8.3 Research

```txt
add_research_slot = 1
add_tech_bonus = {
    bonus = 0.5
    uses = 2
    category = cat_mechanized_equipment
    name = {bonus_name}
}
add_tech_bonus = {
    bonus = 0.75
    uses = 1
    category = armor
    ahead_reduction = 0.5     # reduce ahead-of-time penalty
    name = {bonus_name}
}
add_to_tech_sharing_group = {group_name}
```

### 8.4 Buildings and States

```txt
# Add available building slots
add_extra_state_shared_building_slots = 2

# Build in random state
random_owned_controlled_state = {
    limit = {
        is_core_of = ROOT
        is_owned_by = ROOT
        free_building_slots = {
            building = industrial_complex
            size > 1
            include_locked = yes
        }
    }
    prioritize = { 295 }     # prioritize specific state
    add_building_construction = {
        type = industrial_complex
        level = 2
        instant_build = yes
    }
}

# Build in specific state
random_controlled_state = {
    limit = { ... }
    prioritize = { 295 889 }
    add_building_construction = {
        type = naval_base
        province = {id}
        level = 3
        instant_build = yes
    }
}

# Direct state operation (state ID as key)
{state_id} = {
    add_extra_state_shared_building_slots = 1
    add_building_construction = {
        type = infrastructure
        level = 1
        instant_build = yes
    }
}

# Building types
industrial_complex    # civilian factory
arms_factory          # military factory
dockyard             # shipyard
air_base            # air base
naval_base          # naval base
anti_air_building   # anti-air
radar_station       # radar
synthetic_refinery  # synthetic refinery
fuel_silo           # fuel depot
supply_node         # supply hub
bunker              # bunker
coastal_bunker      # coastal bunker
infrastructure      # infrastructure
railway            # railway

# free_building_slots condition
free_building_slots = {
    building = {type}
    size > {n}
    include_locked = yes    # include locked slots
}
```

### 8.5 Resources

```txt
add_resource = {
    type = {oil|aluminium|rubber|steel|tungsten|chromium}
    amount = {n}
}
```

### 8.6 Railway and Supply

```txt
build_railway = {
    path = { {province_id} {province_id} {province_id} }
}
supply_node = {
    province = {id}
    level = {n}
}
```

### 8.7 Variables

```txt
set_variable = { {var} = {n} }
add_to_variable = { var = {path} value = {n} tooltip = {tt} }
set_temp_variable = { {var} = {n} }
add_to_temp_variable = { {var} = {n} }
check_variable = { {var} = {n} }
check_variable = { {var} > {n} }

# Variable reference paths
ROOT.xxx                    # current country
{gc}.xxx                    # global
{tag}.xxx                   # specific country
{state_id}.xxx             # specific state
{tag}.{modifier}.{field}   # modifier field (Congo model)
global.{varname}           # global variable (Habsburg model)
```

### 8.8 Division Templates

```txt
# Define template in focus reward
completion_reward = {
    division_template = {
        name = "Elite Grenadiers"
        override_model = GER_infantry_div_override
        regiment = { base = infantry size = 4 }
        regiment = { base = infantry size = 3 }
        obsolete = { infantry = { x = 0 y = 0 } }
    }
}
```

### 8.9 Events

```txt
country_event = {
    id = {event_file}.{n}    # file_name.event_number
    days = {n}
    random_days = {n}          # plus/minus random days
    hours = {n}
}

# reference other country event
ROOT = { country_event = { id = ww_congo.1 hours = 0 } }
```

### 8.10 Flags

```txt
set_country_flag = { flag = {name} days = {n} value = 1 }
clr_country_flag = {flag}
set_state_flag = { flag = {name} days = {n} }
set_global_flag = {flag}
```

### 8.11 Cosmetic Tag

```txt
set_cosmetic_tag = {TAG}    # change displayed country name (e.g. HUN_EMPIRE)
```

### 8.12 Autonomy and Compliance

```txt
add_autonomy_score = {
    value = +/-{n}             # positive = towards independence, negative = towards master
    localization = {key}
}
add_compliance = {n}         # increase compliance in occupied territory
```

### 8.13 UI Tooltips

```txt
custom_effect_tooltip = {
    localization_key = {key}
    CHARACTER = {tag}         # character parameter
}
custom_trigger_tooltip = {
    tooltip = {key}_tt
    {trigger}
}
show_ideas_tooltip = {idea}
unlock_decision_category_tooltip = {id}
```

---

## 9. Triggers

### 9.1 Focus-Related

```txt
has_completed_focus = {id}
has_focus_tree = {tree_id}
is_on_going_focus = {focus_id}
```

### 9.2 Political and Ideology

```txt
has_government = {communism|democratic|fascism|neutrality}
is_subject = yes|no
is_subject_of = {TAG}
has_subject = {TAG}
has_subject = yes
original_tag = {TAG}
any_country_with_original_tag = {
    original_tag_to_check = FRA
    has_capitulated = yes
}
```

### 9.3 Territory and States

```txt
controls_state = {id}
is_owned_and_controlled_by = {TAG}
is_owned_by = {id}
is_core_of = {TAG}
is_controlled_by = {TAG}
is_fully_controlled_by = {TAG}
has_full_control_of_state = {id}
is_capital = yes
```

### 9.4 Relations and Factions

```txt
is_in_faction_with = {TAG}
is_faction_leader = yes|no
any_allied_country = { {trigger} }
any_other_country = { {trigger} }
has_war_with = {TAG}
has_war = yes|no
has_capitulated = yes
```

### 9.5 Economic and Industry

```txt
num_of_controlled_factories > {n}
num_of_factories > {n}
num_of_available_buildings = {
    state = {id}
    type = industrial_complex
    size > 0
}
free_building_slots = { ... }
```

### 9.6 Flags

```txt
has_country_flag = {flag}
has_country_flag = {flag} = 1
has_state_flag = {flag}
has_global_flag = {flag}
has_character_flag = {flag}
```

### 9.7 Player and AI

```txt
is_ai = yes|no
is_historical_focus_on = yes
has_dlc = "Gotterdammerung"
```

### 9.8 Special

```txt
is_on_continent = {asia|europe|africa|north_america|south_america|oceania}
is_in_home_area = yes
is_owned_by = ROOT
```

---

## 10. Variables and UI

### 10.1 Conditional Blocks

```txt
# IF/ELSE_IF/ELSE (case-insensitive; both IF and if appear in game files)
if = { limit = { {trigger} } {effect} }
else_if = { limit = { {trigger} } {effect} }
else = { {effect} }

# Loop
while_loop_effect = {
    limit = { {trigger} }
    {effect}
}
```

### 10.2 Random Selection

```txt
random_owned_controlled_state = {
    limit = { {trigger} }
    prioritize = { {id} {id} }
    {effect}
}

random_controlled_state = {
    limit = { {trigger} }
    prioritize = { {id} }
    {effect}
}

random_state = { ... }

random_character = {
    limit = { {trigger} }
    {effect}
}
```

### 10.3 effect_tooltip vs hidden_effect

| Block | Executes | UI Shows |
|-------|----------|----------|
| `completion_reward` | Yes | Yes |
| `hidden_effect` | Yes | No |
| `complete_tooltip` | No | Yes (tooltip only) |
| `effect_tooltip` | No | Yes (preview only) |

---

## 11. Common Pitfalls

### 11.1 ai_will_do default factor is 0

All focuses have `ai_will_do.base` defaulting to 0. AI will NEVER auto-select without setting this.

### 11.2 cancel_if_invalid defaults to yes

When condition becomes invalid, without `cancel_if_invalid = no`, the focus is CANCELLED instead of paused.

### 11.3 available_if_capitulated defaults to no

After capitulation, focus trees are normally unavailable unless explicitly set.

### 11.4 Inner Circle focuses MUST have select_effect

Without `select_effect`, when the `available` condition is not met, the focus pauses with no recovery path.

### 11.5 offset trigger matching order

Multiple `offset` blocks match top-to-bottom. The FIRST matching one takes effect. Ensure all possible countries/states have corresponding offsets.

### 11.6 original_tag case sensitivity

Game `original_tag` trigger is case-sensitive: must match game tag exactly (e.g. `COG` cannot be written as `cog`).

### 11.7 relative_position_id is relative

`relative_position_id = GER_xxx` means the focus x/y is an offset from `GER_xxx` position, not from origin. Watch for cumulative offsets in chain dependencies.

### 11.8 Dynamic modifier variable naming

`add_to_variable = { var = BEL.COG_xxx }` means modify variable inside `BEL`'s country scope. Wrong spelling or nonexistent variables silently fail.

### 11.9 hidden_effect conditionals

Effects inside `hidden_effect` execute UNCONDITIONALLY. If you need conditional execution, nest the if INSIDE hidden_effect.

```txt
# WRONG: if outside hidden_effect does not affect hidden_effect execution
if = { limit = { ... } hidden_effect = { ... } }

# CORRECT: if inside hidden_effect
hidden_effect = {
    if = { limit = { ... } ... }
}
```

### 11.10 joint_focus available timing

`joint_focus` `available` is checked for ANY one member. When one member satisfies it, ALL members see it as available. `joint_trigger` checks if the current country is eligible.

---

## Appendix: Shared Focus Tree File List

| File | Countries | Relationship Model |
|------|-----------|-------------------|
| `nordic_shared.txt` | Finland/Sweden/Denmark/Norway | Equal allies |
| `habsburg_joint.txt` | Austria/Hungary/Czech/etc. | Three modes |
| `congo_shared.txt` | Belgium/Congo | Master-subject |
| `baltic_shared.txt` | Estonia/Latvia/Lithuania | Equal allies |
| `china_shared.txt` | China factions | TBD |
| `generic_joint.txt` | Multiple generic | TBD |

Official Wiki: hoi4.paradoxwikis.com