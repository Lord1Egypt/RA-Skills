-- HD2-Addon: mods/dsh/refscan
--
-- READ-ONLY reference census for Dominator mod work (Q1 clone + Q2 full-auto).
-- Writes nothing to game memory. Dumps, to %LOCALAPPDATA%/Hd2ProjRecon/:
--   refscan_ldld.txt       -- map of every LDLD table header (type -> name/addr/size)
--   refscan_projectiles.txt-- every ProjectileSettings record: parsed + full hex
--   refscan_weapons.txt    -- every ProjectileWeapon record: projtype/function + hex
--   refscan_weapondata.txt -- player WeaponDataComponentData records, full hex
--   refscan_enemy.txt      -- enemy WeaponDataComponent records, full hex (in-mission)
--   refscan_raw_<type>.txt -- bounded raw hex of every OTHER LDLD table
--
-- One run maps the whole layout so a projectile record referenced by NOTHING
-- (weapons + enemy attacks + shrapnel/beam/orbital) can be found offline, and the
-- Q2 fire-mode/cyclic-rate records are captured too.

local state = rawget(_G, "RefScanState")
if state then return end
state = { frames = 0, phase = "init", passes = 0 }
rawset(_G, "RefScanState", state)

local REVISION = "diag-4"

local ok_ffi, ffi = pcall(require, "ffi")
if not ok_ffi or not ffi then state.phase = "no_ffi"; return end

ffi.cdef [[
    void *GetCurrentProcess(void);
    int ReadProcessMemory(void *process, const void *address, void *buffer, size_t size, size_t *read);
    typedef struct {
        void *base; void *allocation_base; uint32_t allocation_protection;
        uint16_t partition; uint16_t reserved; size_t size;
        uint32_t state; uint32_t protection; uint32_t type;
    } DerMemRegion;
    size_t VirtualQuery(const void *address, void *region, size_t size);
    int CreateDirectoryA(const char *path, void *security);
    uint32_t GetLastError(void);
]]

local kernel = ffi.load("kernel32")
local process = kernel.GetCurrentProcess()

-- --------------------------------------------------------------- output ---
local out_dir = nil
do
    local base = os.getenv("LOCALAPPDATA")
    if base then
        local candidate = base .. "/Hd2ProjRecon"
        if kernel.CreateDirectoryA(candidate, nil) ~= 0 or kernel.GetLastError() == 183 then
            out_dir = candidate
        end
    end
end

local NL = string.char(10)
local function wfile(name, text)
    if not out_dir then return end
    local ok, f = pcall(io.open, out_dir .. "/" .. name, "w")
    if ok and f then pcall(f.write, f, text); pcall(f.close, f) end
end
-- Write full binary payload; only for the big tables (hexdump would 3x-expand + freeze).
local function wfile_bin(name, bytes)
    if not out_dir then return end
    local ok, f = pcall(io.open, out_dir .. "/" .. name, "wb")
    if ok and f then pcall(f.write, f, bytes); pcall(f.close, f) end
end
local function log(line)
    print("[RefScan] " .. line)
end

-- ---------------------------------------------------------------- memory ---
local scratch = ffi.new("uint8_t[1048576]")
local read_count = ffi.new("size_t[1]")
local function read_at(address, size)
    if size <= 0 or size > 1048576 then return nil end
    if kernel.ReadProcessMemory(process, ffi.cast("const void *", address), scratch, size, read_count) == 0 then return nil end
    if read_count[0] ~= size then return nil end
    return ffi.string(scratch, size)
end

local region = ffi.new("DerMemRegion[1]")
local function region_info(address)
    if kernel.VirtualQuery(ffi.cast("const void *", address), ffi.cast("void *", region), ffi.sizeof(region[0])) ~= ffi.sizeof(region[0]) then return nil end
    return { base = tonumber(ffi.cast("uintptr_t", region[0].base)),
             size = tonumber(region[0].size), state = tonumber(region[0].state),
             protection = tonumber(region[0].protection), type = tonumber(region[0].type) }
end

local function u32_at(s, i)
    local a, b, c, d = s:byte(i, i + 3)
    if not d then return nil end
    return a + b * 256 + c * 65536 + d * 16777216
end

local function u64_at(s, i)
    local lo, hi = u32_at(s, i), u32_at(s, i + 4)
    if not lo or not hi then return nil end
    return lo + hi * 4294967296
end

local function bits_to_f32(bits)
    local sign = 1
    if bits >= 2147483648 then sign = -1; bits = bits - 2147483648 end
    local exp = math.floor(bits / 8388608)
    local mant = bits - exp * 8388608
    if exp == 255 then
        if mant == 0 then return sign * math.huge end
        return 0 / 0
    end
    if exp == 0 then
        if mant == 0 then return sign * 0.0 end
        return sign * mant * 2 ^ -149
    end
    return sign * (1 + mant / 8388608) * 2 ^ (exp - 127)
end

local function f32_at(s, i)
    local a, b, c, d = s:byte(i, i + 3)
    if not d then return nil end
    return bits_to_f32(a + b * 256 + c * 65536 + d * 16777216)
end

-- ------------------------------------------------------------ table hashes ---
local T_PROJECTILE   = 0xBD4042C2  -- ProjectileSettings
local T_PROJ_WEAPON  = 0x45171B68  -- ProjectileWeaponComponentData
local T_WEAPON_DATA  = 0x88E4DBB1  -- WeaponDataComponentData (player)
local T_ENEMY_WEAPON = 0xd25fc7f7  -- WeaponDataComponent (enemy counterpart)
local T_EXPLOSION    = 0x2AEA2592  -- ExplosionSettings (shrapnel sub-projectiles)
local T_WEAPROUNDS   = 0x66081072  -- WeaponRoundsComponentData
local T_DAMAGE       = 0xE0A72CF0  -- DamageSettings
local T_MAGAZINE     = 0xFB8D88A3  -- WeaponMagazineComponentData
local T_HEALTH       = 0xB3915DE3  -- HealthComponentData (11 MB; skip raw)

local LDLD_MAGIC = string.char(0x4C, 0x44, 0x4C, 0x44, 1, 0, 0, 0)
local HEADER_BYTES = 24

local TBL_NAMES = {
    [T_PROJECTILE] = "ProjectileSettings",
    [T_PROJ_WEAPON] = "ProjectileWeaponComponentData",
    [T_WEAPON_DATA] = "WeaponDataComponentData",
    [T_ENEMY_WEAPON] = "WeaponDataComponent(enemy)",
    [T_EXPLOSION] = "ExplosionSettings",
    [T_WEAPROUNDS] = "WeaponRoundsComponentData",
    [T_DAMAGE] = "DamageSettings",
    [T_MAGAZINE] = "WeaponMagazineComponentData",
    [T_HEALTH] = "HealthComponentData",
}

-- Tables we dump full raw hex for (projectile-reference cross-ref). Everything
-- else is still mapped in refscan_ldld.txt but only bounded-raw-dumped.
local RAW_TARGETS = {
    [T_EXPLOSION] = true, [T_WEAPROUNDS] = true, [T_DAMAGE] = true,
    [T_MAGAZINE] = true,
}

-- ------------------------------------------------------------- region walk ---
local self_anchor = nil
do
    local sig = LDLD_MAGIC .. string.char(0, 0, 0, 0)
    local ok, p = pcall(function()
        return tonumber(ffi.cast("uintptr_t", ffi.cast("const char *", sig)))
    end)
    if ok and p and p > 0 then self_anchor = p end
end

local function is_readable(protection)
    return protection == 2 or protection == 4 or protection == 8
        or protection == 32 or protection == 64 or protection == 128
end

local function collect_regions()
    local list = {}
    local address = 65536
    while address < 2 ^ 47 do
        local r = region_info(address)
        if not r or not r.size or r.size <= 0 then break end
        if r.state == 4096 and is_readable(r.protection)
            and (r.type == 131072 or r.type == 262144) and r.size >= 65536 then
            if not (self_anchor and r.base <= self_anchor and self_anchor < r.base + r.size) then
                list[#list + 1] = { base = r.base, size = r.size }
            end
        end
        local nx = r.base + r.size
        if nx <= address then break end
        address = nx
    end
    return list
end

local SCAN_BUDGET = 0.004
local CHUNK = 262144
local OVERLAP = 16

local region_list = nil
local region_index = 1
local region_offset = 0
local previous = ""
local scan_done = false

local ldld_headers = {}
local ldld_seen = {}
local projectiles = nil
local proj_weapon = nil

local function examine(window_base, window)
    local from = 1
    while true do
        local i = string.find(window, LDLD_MAGIC, from, true)
        if not i then break end
        local abs = window_base + i - 1
        from = i + 1
        local skip = false
        if self_anchor and math.abs(abs - self_anchor) < 4096 then skip = true end
        if not skip and not ldld_seen[abs] then
            ldld_seen[abs] = true
            local hdr = read_at(abs, HEADER_BYTES)
            if hdr then
                local typ = u32_at(hdr, 9)
                local sz = u32_at(hdr, 13)
                if typ and sz and sz >= 16 and sz <= 16777216 and typ ~= 0 then
                    ldld_headers[#ldld_headers + 1] = { addr = abs, type = typ, size = sz }
                end
            end
        end
    end
end

local function scan_step()
    if scan_done then return end
    if not region_list then
        region_list = collect_regions()
        log(string.format("%d regions to scan", #region_list))
        return
    end
    local deadline = os.clock() + SCAN_BUDGET
    while os.clock() < deadline do
        local r = region_list[region_index]
        if not r then scan_done = true; return end
        local remaining = r.size - region_offset
        if remaining <= 0 then
            region_index = region_index + 1
            region_offset = 0
            previous = ""
        else
            local want = CHUNK
            if want > remaining then want = remaining end
            local buf = read_at(r.base + region_offset, want)
            if buf then
                local wb = r.base + region_offset - #previous
                examine(wb, previous .. buf)
                previous = buf:sub(-OVERLAP)
            else
                previous = ""
            end
            region_offset = region_offset + want
        end
    end
end

-- ------------------------------------------------------------- raw helpers ---
local function read_payload(h, maxBytes)
    local want = h.size
    if maxBytes and want > maxBytes then want = maxBytes end
    local out = {}
    local got = 0
    while got < want do
        local n = want - got
        if n > 1048576 then n = 1048576 end
        local chunk = read_at(h.addr + HEADER_BYTES + got, n)
        if not chunk then return nil end
        out[#out + 1] = chunk
        got = got + n
    end
    return table.concat(out)
end

local function hexdump(bytes)
    local lines = {}
    for off = 0, #bytes - 1, 16 do
        local chunk = bytes:sub(off + 1, off + 16)
        local hex = {}
        for i = 1, #chunk do hex[#hex + 1] = string.format("%02X", chunk:byte(i)) end
        lines[#lines + 1] = string.format("%08X  %s", off, table.concat(hex, " "))
    end
    return table.concat(lines, NL)
end

-- --------------------------------------------------------- parsed walkers ---
-- ProjectileSettings: 24-byte LDLD header, then 16-byte DLArray descriptor
-- (u64 ptr, u64 count), then cnt * stride records. First u64 may be absolute or
-- a relative offset from magic+24 (mirrors Dominator's validate_block).
local function resolve_projectiles(h)
    local buf = read_at(h.addr, HEADER_BYTES + 16)
    if not buf then return nil end
    local ver = u32_at(buf, 5)
    local typ = u32_at(buf, 9)
    local size = u32_at(buf, 13)
    if ver ~= 1 or typ ~= T_PROJECTILE then return nil end
    if not size or size < 1024 or size > 16777216 then return nil end
    local f1 = u64_at(buf, 25)
    local cnt = u64_at(buf, 33)
    if not f1 or not cnt or cnt < 32 or cnt > 65536 then return nil end
    if (size - 16) % cnt ~= 0 then return nil end
    local stride = math.floor((size - 16) / cnt)
    if stride < 64 or stride > 4096 then return nil end
    local candidates = { f1, h.addr + 24 + f1 }
    for _, ptr in ipairs(candidates) do
        if ptr >= 65536 and ptr < 2 ^ 47 then
            local probe = read_at(ptr, 8)
            if probe and u32_at(probe, 1) and u32_at(probe, 1) < 20000 then
                return { records = ptr, count = cnt, stride = stride }
            end
        end
    end
    return nil
end

-- ProjectileWeapon: bucket array (u64 entity, u32 slot, u32 pad) then 616-byte records.
local function resolve_projectile_weapon(h)
    local buf = read_at(h.addr + HEADER_BYTES, h.size)
    if not buf then return nil end
    local count, offset, total = 0, 0, #buf
    while offset + 16 <= total do
        local pad = u32_at(buf, offset + 13)
        local slot = u32_at(buf, offset + 9)
        if pad ~= 0 or slot > 100000 then break end
        count = count + 1
        offset = offset + 16
    end
    local records = math.floor((total - count * 16) / 616)
    if records < 1 or records > 10000 then return nil end
    return { records = h.addr + HEADER_BYTES + count * 16, count = records, buckets = count }
end

-- Keyed table (WeaponData / enemy WeaponData): same bucket layout, stride 1232.
local function resolve_keyed(h, stride)
    local buf = read_at(h.addr + HEADER_BYTES, h.size)
    if not buf then return nil end
    local count, offset, total = 0, 0, #buf
    while offset + 16 <= total do
        local pad = u32_at(buf, offset + 13)
        local slot = u32_at(buf, offset + 9)
        if pad ~= 0 or slot > 100000 then break end
        count = count + 1
        offset = offset + 16
    end
    local records = math.floor((total - count * 16) / stride)
    if records < 1 or records > 10000 then return nil end
    return { records = h.addr + HEADER_BYTES + count * 16, count = records, buckets = count, stride = stride }
end

local function dump_projectiles()
    if not projectiles then return end
    local lines = {}
    lines[#lines + 1] = string.format("records=%d stride=%d (addr=0x%X)", projectiles.count, projectiles.stride, projectiles.records)
    for i = 0, projectiles.count - 1 do
        local rec = read_at(projectiles.records + i * projectiles.stride, projectiles.stride)
        if rec then
            lines[#lines + 1] = string.format(
                "record%d type=%d name=0x%08X speed=%.1f mass=%.1f drag=%.2f grav=%.2f life=%.3f arming=%.2f dmg=%s expl_imp=%s expl_exp=%s",
                i, u32_at(rec, 1) or -1, u32_at(rec, 5) or 0,
                f32_at(rec, 33) or -1, f32_at(rec, 37) or -1,
                f32_at(rec, 41) or -1, f32_at(rec, 45) or -1, f32_at(rec, 53) or -1,
                f32_at(rec, 161) or -1, tostring(u32_at(rec, 61)), tostring(u32_at(rec, 145)),
                tostring(u32_at(rec, 157)))
            lines[#lines + 1] = hexdump(rec)
        end
    end
    wfile("refscan_projectiles.txt", table.concat(lines, NL) .. NL)
    log(string.format("dumped %d projectile records", projectiles.count))
end

local function dump_projectile_weapon()
    if not proj_weapon then return end
    local lines = {}
    lines[#lines + 1] = string.format("buckets=%d records=%d stride=616", proj_weapon.buckets, proj_weapon.count)
    for i = 0, proj_weapon.count - 1 do
        local rec = read_at(proj_weapon.records + i * 616, 616)
        if rec then
            lines[#lines + 1] = string.format("--- record %d (projtype=%d function=%d) ---", i,
                u32_at(rec, 1) or -1, u32_at(rec, 577) or -1)
            lines[#lines + 1] = hexdump(rec)
        end
    end
    wfile("refscan_weapons.txt", table.concat(lines, NL) .. NL)
    log(string.format("dumped %d projectile-weapon records", proj_weapon.count))
end

local function dump_keyed(name, tbl)
    if not tbl then return end
    local lines = {}
    lines[#lines + 1] = string.format("buckets=%d records=%d stride=%d", tbl.buckets, tbl.count, tbl.stride)
    for i = 0, tbl.count - 1 do
        local rec = read_at(tbl.records + i * tbl.stride, tbl.stride)
        if rec then
            lines[#lines + 1] = string.format("--- record %d ---", i)
            lines[#lines + 1] = hexdump(rec)
        end
    end
    wfile(name, table.concat(lines, NL) .. NL)
    log(string.format("dumped %d records to %s", tbl.count, name))
end

local RAW_CAP = 262144   -- 256 KB raw hex cap per table (keeps dump small, no freeze)

local function dump_all()
    -- map
    local lines = {}
    for _, h in ipairs(ldld_headers) do
        lines[#lines + 1] = string.format("type=0x%08X %-28s addr=0x%X size=%d",
            h.type, TBL_NAMES[h.type] or "unknown", h.addr, h.size)
    end
    wfile("refscan_ldld.txt", table.concat(lines, NL) .. NL)

    -- resolve the parsed tables
    local weapondata, enemy = nil, nil
    projectiles, proj_weapon = nil, nil
    for _, h in ipairs(ldld_headers) do
        if h.type == T_PROJECTILE and not projectiles then
            projectiles = resolve_projectiles(h)
        elseif h.type == T_PROJ_WEAPON and not proj_weapon then
            proj_weapon = resolve_projectile_weapon(h)
        elseif h.type == T_WEAPON_DATA and not weapondata then
            weapondata = resolve_keyed(h, 1232)
        elseif h.type == T_ENEMY_WEAPON and not enemy then
            enemy = resolve_keyed(h, 1232)
        end
    end

    dump_projectiles()
    dump_projectile_weapon()
    dump_keyed("refscan_weapondata.txt", weapondata)
    dump_keyed("refscan_enemy.txt", enemy)

    -- bounded raw hex of the small tables; FULL BINARY of the big ones (enemy data)
    local seen = {}
    for _, h in ipairs(ldld_headers) do
        if h.type ~= T_PROJECTILE and h.type ~= T_PROJ_WEAPON
            and h.type ~= T_WEAPON_DATA and h.type ~= T_ENEMY_WEAPON
            and h.type ~= T_HEALTH then
            if not seen[h.type] then
                seen[h.type] = true
                local nm = TBL_NAMES[h.type] or string.format("0x%08X", h.type)
                local safe = nm:gsub("[^%w%-]", "_")
                if h.size > RAW_CAP then
                    -- big table: full binary payload (no hexdump, no freeze)
                    local payload = read_payload(h, nil)
                    if payload then
                        wfile_bin("refscan_bin_" .. safe .. ".bin", payload)
                        log(string.format("bin: %s (%d bytes)", nm, #payload))
                    end
                else
                    local payload = read_payload(h, RAW_CAP)
                    if payload then
                        local body = string.format("type=0x%08X %s addr=0x%X size=%d (payload shown %d)\n",
                            h.type, nm, h.addr, h.size, #payload)
                        body = body .. hexdump(payload)
                        wfile("refscan_raw_" .. safe .. ".txt", body)
                    end
                end
            end
        end
    end

    log(string.format("pass %d done: headers=%d projectiles=%s proj_weapon=%s weapondata=%s enemy=%s",
        state.passes, #ldld_headers,
        tostring(projectiles ~= nil), tostring(proj_weapon ~= nil),
        tostring(weapondata ~= nil), tostring(enemy ~= nil)))
end

-- ------------------------------------------------------------------ drive ---
-- Full walk once, dump, then re-walk periodically (bounded) to catch the enemy
-- table once it loads in-mission. Self-terminates; no permanent scanner.
local SCAN_GAP_FRAMES = 2700   -- ~45s between passes
local MAX_PASSES = 8
local next_rescan = 0

local original_update = update
if type(original_update) == "function" then
    function update(...)
        state.frames = state.frames + 1
        if state.phase == "scanning" and state.frames >= 60 then
            if not scan_done then
                if (state.frames % 2) == 0 then
                    local ok, err = pcall(scan_step)
                    if not ok then scan_done = true; log("scan error: " .. tostring(err)) end
                end
            elseif state.frames >= next_rescan then
                state.passes = state.passes + 1
                local enemy_found = false
                for _, h in ipairs(ldld_headers) do
                    if h.type == T_ENEMY_WEAPON then enemy_found = true end
                end
                local ok, err = pcall(dump_all)
                if not ok then log("dump error: " .. tostring(err)) end
                if enemy_found or state.passes >= MAX_PASSES then
                    state.phase = "done"
                    log("refscan complete (enemy=" .. tostring(enemy_found) .. ")")
                else
                    -- re-walk fresh for the next pass
                    next_rescan = state.frames + SCAN_GAP_FRAMES
                    scan_done = false
                    region_list = nil
                    region_index = 1
                    region_offset = 0
                    previous = ""
                    ldld_headers = {}
                    ldld_seen = {}
                end
            end
        end
        return original_update(...)
    end
    log("refscan diag-4 loaded; will census memory, dump, then hunt enemy table")
    state.phase = "scanning"
end

return { revision = REVISION, state = state }
