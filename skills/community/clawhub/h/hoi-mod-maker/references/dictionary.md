# HOI4 Effects & Triggers Dictionary

Source: Official HOI4 documentation (`effects_documentation.md` / `triggers_documentation.md`)

---

## Effects

Total: 169 curated entries

| Effect | Scope | Description |
|--------|-------|-------------|
| `add_political_power` | COUNTRY | add political power to country |
| `add_command_power` | COUNTRY | add command power to country |
| `add_stability` | COUNTRY | Adds the stability to the country in scope |
| `add_war_support` | COUNTRY | Adds the war support to the country in scope |
| `add_popularity` | COUNTRY | add popularity to an ideology in a country |
| `add_ideas` | COUNTRY | add idea(s) to country |
| `add_timed_idea` | COUNTRY | Add a time-limited idea to country in scope |
| `army_experience` | COUNTRY | add army experience for country |
| `navy_experience` | COUNTRY | add naval experience for country |
| `air_experience` | COUNTRY | add air experience for country |
| `add_research_slot` | COUNTRY | Adds a research slot (negative values subtracts) |
| `add_tech_bonus` | COUNTRY | adds a limited use tech bonus |
| `add_doctrine_cost_reduction` | COUNTRY | adds a limited use cost reduction for doctrines |
| `add_manpower` | STATE, COUNTRY | Adds manpower to the country in scope or locally on a state |
| `add_building_construction` | STATE | Starts building construction for amount of levels in specified state |
| `add_extra_state_shared_building_slots` | STATE | add extra shared building slot to state |
| `add_resource` | STATE, COUNTRY | Adds/removes resource production to state |
| `build_railway` | any | Builds/adds railway level between two provinces or along a path |
| `country_event` | COUNTRY | Fires a country event |
| `add_dynamic_modifier` | STATE, COUNTRY, CHARACTER | adds a dynamic modifier to the containing scope |
| `remove_dynamic_modifier` | STATE, COUNTRY, CHARACTER | removes a dynamic modifier |
| `force_update_dynamic_modifier` | STATE, COUNTRY, CHARACTER | updates the modifiers in current scope |
| `set_country_flag` | COUNTRY | set country flag |
| `clr_country_flag` | COUNTRY | clear country flag |
| `set_state_flag` | STATE | set state flag |
| `set_global_flag` | any | set global flag |
| `set_cosmetic_tag` | COUNTRY | Sets country cosmetic tag |
| `drop_cosmetic_tag` | COUNTRY | Drops country cosmetic tag |
| `unlock_national_focus` | COUNTRY | unlocks a focus for a country |
| `complete_national_focus` | COUNTRY | completes a focus for a country |
| `uncomplete_national_focus` | COUNTRY | uncompletes a focus for a country |
| `load_focus_tree` | COUNTRY | Sets what focus tree a country uses |
| `reduce_focus_completion_cost` | COUNTRY | Reduce the cost needed to complete a specific focus |
| `add_autonomy_score` | COUNTRY | Adds exact freedom score to the autonomy |
| `add_autonomy_ratio` | COUNTRY | Adds % freedom score to the autonomy |
| `set_autonomy` | COUNTRY | makes autonomy of specified level and country |
| `release_autonomy` | COUNTRY | releases specified country with specified level of autonomy |
| `add_compliance` | STATE | add compliance to a state |
| `add_resistance` | STATE | add resistance to a state |
| `add_state_core` | COUNTRY | add core on state |
| `add_state_claim` | COUNTRY | add claim on state |
| `remove_state_core` | COUNTRY | remove core on state |
| `remove_state_claim` | COUNTRY | remove claim on state |
| `annex_country` | COUNTRY | annex a country |
| `puppet` | COUNTRY | Puppets specified country |
| `release_puppet` | COUNTRY | releases specified country as puppet using states you own |
| `end_puppet` | COUNTRY | Stops specified country being a puppet of current country |
| `declare_war_on` | COUNTRY | declares war on specified country |
| `add_to_war` | COUNTRY | adds country to the specified war |
| `create_faction` | COUNTRY | creates a faction |
| `dismantle_faction` | COUNTRY | dismantles faction led by current country |
| `add_to_faction` | COUNTRY | adds specified country to faction |
| `leave_faction` | COUNTRY | Country leaves the faction |
| `give_guarantee` | COUNTRY | guarantees specified country |
| `give_military_access` | COUNTRY | gives military access to the specified country |
| `give_resource_rights` | COUNTRY | Gives rights to take resources from specified state |
| `set_variable` | any | Sets a variable to a value or another variable |
| `add_to_variable` | any | Adds a value or a variable to another one |
| `set_temp_variable` | any | Sets a temp variable to a value or another variable |
| `add_to_temp_variable` | any | Adds a value or a variable to a temp variable |
| `clear_variable` | any | Clears a variable |
| `multiply_variable` | any | Multiplies a variable to a value or another variable |
| `subtract_from_variable` | any | Subtracts a value or a variable to another one |
| `hidden_effect` | any | Effect not shown in tooltips |
| `effect_tooltip` | any | Shows just tooltip of effects |
| `custom_effect_tooltip` | any | custom_effect_tooltip = MY_TOOLTIP |
| `if` | any | a conditional effect |
| `while_loop_effect` | any | Runs the effect as long as a trigger is true |
| `random` | any | a random effect |
| `random_list` | any | Picks a random effect from the list based on weight |
| `random_controlled_state` | COUNTRY | Executes children effects on random controlled state |
| `random_owned_controlled_state` | COUNTRY | Executes children effects on random owned and controlled state |
| `random_state` | any | Executes children effects on a random state |
| `every_state` | any | Executes children effects on every State |
| `every_owned_state` | COUNTRY | Executes children effects on every State owned by the country |
| `every_controlled_state` | COUNTRY | Executes children effects on every State controlled by the country |
| `every_allied_country` | COUNTRY | Executes effects on every allied country |
| `every_enemy_country` | COUNTRY | Executes children effects on every enemy Country |
| `every_subject_country` | COUNTRY | Executes children effects on every subject Country |
| `show_ideas_tooltip` | COUNTRY | show what idea does |
| `unlock_decision_tooltip` | COUNTRY | show what decision does |
| `unlock_decision_category_tooltip` | COUNTRY | localizes name of category and displays tooltip |
| `set_politics` | COUNTRY | set_politics |
| `hold_election` | COUNTRY | Immediately holds an election in the target country |
| `set_party_name` | COUNTRY | change partyname for an ideology in a country |
| `set_political_party` | COUNTRY | set popularity of a political party |
| `add_to_tech_sharing_group` | COUNTRY | Adds country to technology sharing group |
| `set_occupation_law` | STATE, COUNTRY | Sets the occupation law |
| `set_resistance` | STATE | set resistance of a state |
| `cancel_resistance` | STATE | cancels resistance activity for a core country |
| `create_intelligence_agency` | COUNTRY | create an Intelligence Agency |
| `upgrade_intelligence_agency` | COUNTRY | add an upgrade to the Intelligence Agency |
| `division_template` | COUNTRY | add a division template to country |
| `delete_units` | COUNTRY | deletes units that uses a specific template |
| `add_units_to_division_template` | COUNTRY | Add units to division template for a country |
| `add_equipment_to_stockpile` | COUNTRY | Add or remove equipment from country stockpiles |
| `add_equipment_bonus` | COUNTRY | Adds the specified equipment bonuses |
| `add_equipment_production` | COUNTRY | Creates a new production line for the input equipment |
| `modify_building_resources` | COUNTRY | Modifies resource output of specific building |
| `set_nationality` | COUNTRY, CHARACTER | Transfer from one country to another for the character |
| `add_nationality` | CHARACTER | Add the specified nationality to the scoped-in operative |
| `add_relation_modifier` | COUNTRY | Adds a static modifier between current scope and target |
| `add_opinion_modifier` | COUNTRY | Add opinion modifier(s) to target(s) |
| `remove_opinion_modifier` | COUNTRY | Remove opinion modifier from target |
| `add_collaboration` | COUNTRY | Adds the collaboration in a target country |
| `add_advisor_role` | COUNTRY, CHARACTER | add advisor role to character |
| `remove_advisor_role` | COUNTRY, CHARACTER | remove advisor role from character |
| `add_country_leader_role` | COUNTRY, CHARACTER | add country leader role to character |
| `remove_country_leader_role` | COUNTRY, CHARACTER | Remove country leader role from character |
| `add_country_leader_trait` | COUNTRY, CHARACTER | Add country leader trait |
| `remove_country_leader_trait` | COUNTRY, CHARACTER | Remove country leader trait |
| `swap_country_leader_traits` | CHARACTER | swap 2 traits on a country leader |
| `set_country_leader_name` | COUNTRY | changes the name of country leader |
| `set_country_leader_description` | COUNTRY | changes the description of country leader |
| `set_country_leader_portrait` | COUNTRY | changes the portrait of country leader |
| `add_corps_commander_role` | COUNTRY, CHARACTER | add corps commander role to character |
| `add_field_marshal_role` | COUNTRY, CHARACTER | add field marshall role to character |
| `add_naval_commander_role` | COUNTRY, CHARACTER | Add naval commander to character |
| `set_province_controller` | COUNTRY | set controller for province |
| `set_state_controller` | COUNTRY | set controller for state |
| `set_state_owner` | COUNTRY | set owner for state |
| `set_research_slots` | COUNTRY | Sets the number of research slots |
| `add_named_threat` | COUNTRY | Adds country threat |
| `add_threat` | COUNTRY | Adds country threat |
| `retire_character` | COUNTRY | Un-assigns a character from a nation |
| `promote_character` | COUNTRY, CHARACTER | promotes character to the head of their political party |
| `ai_message` | COUNTRY | ai message |
| `log` | any | Print message to game.log, console |
| `activate_decision` | COUNTRY | Activates specified decision for scope country |
| `activate_mission` | COUNTRY | Activates mission, ignoring normal trigger conditions |
| `remove_mission` | COUNTRY | Removes mission without running complete or timeout effects |
| `start_civil_war` | COUNTRY | start a civil war |
| `set_rule` | COUNTRY | Adds rule to country |
| `clear_rule` | COUNTRY | Clears rule added by set_rule |
| `set_party_rule` | COUNTRY | Adds rule to the country's party |
| `set_major` | COUNTRY | Sets mandatory major country flag |
| `set_capital` | COUNTRY | move capital to state |
| `become_exiled_in` | COUNTRY | Become exile in target nation |
| `end_exile` | COUNTRY | Ends the exile of the current scope's country |
| `remove_exile_tag` | CHARACTER | remove exile tag from scope unit leader |
| `set_border_war` | STATE | starts a border war in a state |
| `start_border_war` | any | start a border war between two states |
| `cancel_border_war` | any | cancel border war between two states |
| `damage_building` | STATE, COUNTRY | Damages a building in a targeted state or province |
| `remove_building` | STATE, COUNTRY | Removes a building in a targeted state or province |
| `add_mines` | COUNTRY | Add mines to a strategic region |
| `launch_nuke` | COUNTRY | launch nuke at a state |
| `send_equipment` | COUNTRY | Sends to target scope specified amount of equipment |
| `send_equipment_fraction` | COUNTRY | Sends to target scope specified fraction of equipment |
| `add_fuel` | COUNTRY | add fuel to the country |
| `set_fuel` | COUNTRY | set fuel for country |
| `set_fuel_ratio` | COUNTRY | Set country's current fuel ratio relative to its capacity |
| `add_nuclear_bombs` | COUNTRY | add nukes to country |
| `set_technology` | COUNTRY | sets technology level(s) on country |
| `inherit_technology` | COUNTRY | Copies over technology state from target |
| `add_breakthrough_progress` | COUNTRY | Add breakthrough progress to one specialization |
| `add_breakthrough_points` | COUNTRY | Add breakthrough points to one specialization |

---

## Triggers

Total: 79 curated entries

| Trigger | Scope | Description |
|---------|-------|-------------|
| `has_completed_focus` | COUNTRY | has country completed focus |
| `has_focus_tree` | COUNTRY | Does current country have the specified focus tree |
| `has_government` | COUNTRY | does country government belong to ideology group |
| `original_tag` | COUNTRY | original tag is (for civil wars checks) |
| `is_subject` | COUNTRY | Checks if the country is subject of any other country |
| `is_subject_of` | COUNTRY | Checks if the country is subject of specified country |
| `has_subject` | COUNTRY | Checks if the country has for subject the given country |
| `has_war` | COUNTRY | is country at war |
| `has_war_with` | COUNTRY | is countries at war |
| `has_capitulated` | COUNTRY | checks if the country has capitulated |
| `is_in_faction_with` | COUNTRY | check if member of same faction as specified country |
| `is_faction_leader` | COUNTRY | check if country leads a faction |
| `any_allied_country` | COUNTRY | Check if any allied country meets the trigger |
| `any_other_country` | any | check if any other country meets the trigger |
| `any_country` | any | check if any country meets the trigger |
| `any_enemy_country` | COUNTRY | check if any enemy country meets the trigger |
| `any_neighbor_country` | COUNTRY | check if any neighbor country meets the trigger |
| `any_subject_country` | COUNTRY | check if any subject country meets the trigger |
| `controls_state` | COUNTRY | check controller for state(s) |
| `is_owned_and_controlled_by` | STATE | check if state is owned by |
| `is_owned_by` | STATE | check if state is owned by |
| `is_core_of` | STATE | Checks if state is core of country |
| `is_controlled_by` | STATE | check if state is controlled by |
| `is_fully_controlled_by` | STATE | Checks if state is fully controlled by specified tag |
| `is_capital` | STATE | Is scope state a capital |
| `has_full_control_of_state` | COUNTRY | check controller for state(s) |
| `is_on_continent` | STATE | is state located on continent |
| `is_in_home_area` | STATE | Checks if first province is connected to capital |
| `is_coastal` | STATE | check if state is coastal |
| `num_of_controlled_factories` | COUNTRY | check the number of factories in controlled states |
| `num_of_factories` | COUNTRY | Check amount of available factories |
| `free_building_slots` | STATE | checks building for available construction levels |
| `has_country_flag` | COUNTRY | has country flag been set |
| `has_state_flag` | STATE | has state flag been set |
| `has_global_flag` | any | has global flag been set |
| `has_character_flag` | CHARACTER | has a character flag been set |
| `is_ai` | COUNTRY | Checks if country is AI controlled |
| `is_historical_focus_on` | any | check if the historical focus is active |
| `has_dlc` | any | Checks if player has a DLC |
| `has_dynamic_modifier` | STATE, COUNTRY, CHARACTER | has a dynamic modifier |
| `check_variable` | any | Compares a variable to a number or another variable |
| `has_variable` | any | Checks if a variable exists in a scope |
| `has_country_leader` | COUNTRY | check if country has leader with specified ID |
| `has_political_power` | COUNTRY | check amount of political power |
| `has_stability` | COUNTRY | check value of stability 0-1 |
| `has_war_support` | COUNTRY | check value of war_support 0-1 |
| `has_manpower` | COUNTRY | check amount of manpower |
| `has_equipment` | COUNTRY | checks for amount of equipment stored |
| `has_navy_size` | COUNTRY | Checks for amount of ships |
| `has_army_size` | COUNTRY | checks for amount of divisions |
| `has_opinion` | COUNTRY | check what opinion the country has towards a specified country |
| `has_tech_bonus` | COUNTRY | checks if the country has a bonus for the specified technology |
| `is_exiled_in` | COUNTRY | Checks if scope country is a government in exile in target tag |
| `has_resistance` | STATE | returns true if state has a resistance |
| `is_claimed_by` | STATE | Checks if state is claimed by country |
| `owns_state` | COUNTRY | check owner for state(s) |
| `has_border_war` | STATE, COUNTRY | Checks if there is any border wars for country/state |
| `is_demilitarized_zone` | STATE | checks if a state is a demilitarized zone |
| `has_template` | COUNTRY | Check if country has a division template of specific name |
| `has_character` | COUNTRY | Returns true if scoped country has character |
| `has_attache` | COUNTRY | Has attache from any other country |

---

## Key Effects Examples

### add_building_construction

```txt
add_building_construction = {
    type = industrial_complex
    level = 2
    instant_build = yes
}

# For specific state
{state_id} = {
    add_building_construction = {
        type = infrastructure
        level = 1
        instant_build = yes
    }
}
```

### add_timed_idea

```txt
add_timed_idea = {
    idea = my_idea_id
    days = 365
}
# or
add_timed_idea = {
    idea = my_idea_id
    years = 1
    months = 2
    days = 5
}
```

### country_event

```txt
country_event = {
    id = germany.75
    days = 5
    random_days = 2
}
```

### add_tech_bonus

```txt
add_tech_bonus = {
    bonus = 0.5
    uses = 2
    category = cat_mechanized_equipment
    name = bonus_name
}

add_tech_bonus = {
    bonus = 0.75
    uses = 1
    category = armor
    ahead_reduction = 0.5
    name = bonus_name
}
```

### random_owned_controlled_state

```txt
random_owned_controlled_state = {
    limit = {
        is_core_of = ROOT
        free_building_slots = {
            building = industrial_complex
            size > 0
            include_locked = yes
        }
    }
    prioritize = { 295 }
    add_extra_state_shared_building_slots = 2
    add_building_construction = {
        type = arms_factory
        level = 2
        instant_build = yes
    }
}
```

### add_to_variable

```txt
# Local variable
add_to_variable = { var = my_var value = 10 }

# Global variable
add_to_variable = { global.HABSBURG_economy_consumer_goods_factor = -0.1 }

# Cross-country modifier
add_to_variable = {
    var = BEL.COG_belgian_congo_colonial_dynamic_modifier_research_speed_factor
    value = 0.03
}
```

### set_technology

```txt
set_technology = {
    infantry_weapons = 1
    cavalry_1 = 1
    tech_support = 1
    tech_engineers = 1
}
```

---

## Key Triggers Examples

### has_completed_focus

```txt
has_completed_focus = POL_seize_control_of_the_state
```

### original_tag

```txt
# Case-sensitive: must use exact game tag
original_tag = COG    # CORRECT
original_tag = cog     # WRONG
```

### is_subject_of

```txt
is_subject_of = GER
```

### free_building_slots

```txt
free_building_slots = {
    building = industrial_complex
    size > 0
    include_locked = yes
}
```

### check_variable

```txt
check_variable = { global.HABSBURG_economy_consumer_goods_factor > 0.5 }
check_variable = { my_var = 42 }
check_variable = { my_var > 10 }
```