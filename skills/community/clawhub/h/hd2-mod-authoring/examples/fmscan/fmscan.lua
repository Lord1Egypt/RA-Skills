-- HD2-Addon: mods/dsh/fmscan
--
-- READ-ONLY value-scan for the Dominator's fire-mode record (Q2 full-auto).
-- Writes NOTHING to game memory. Scans readable memory for the fire-mode
-- fingerprint — the mode array [single=2, burst=3, none=0] at +0x70/+0x74/+0x78
-- and TertiaryFireMode=0 at +0x7C of a ~144-byte (0x90) record — and dumps each
-- candidate record to %LOCALAPPDATA%/Hd2ProjRecon/fmscan_records.txt.
--
-- Purpose: locate the fire-mode record so the full-auto write (TertiaryFireMode
-- +0x7C -> 1) and the cyclic-rate field can be mapped. The record's type hash is
-- unidentified, so it is found by value fingerprint, not LDLD magic.

local state = rawget(_G, "FMScanState")
if state then return end
state = { frames = 0, phase = "init", hits = 0 }
rawset(_G, "FMScanState", state)

local REVISION = "fmscan-1"

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

-- ---------------------------------------------------------------- output ---
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
local function log(line) print("[FMScan] " .. line) end

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

-- skip our own Lua heap
local self_anchor = nil
do
    local sig = "FMScanState"
    local ok, p = pcall(function() return tonumber(ffi.cast("uintptr_t", ffi.cast("const char *", sig))) end)
    if ok and p and p > 0 then self_anchor = p end
end

-- ------------------------------------------------------------- region walk ---
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
local OVERLAP = 128          -- 0x80, so records spanning a chunk boundary are caught

local region_list = nil
local region_index = 1
local region_offset = 0
local previous = ""
local scan_done = false
local seen = {}
local hits = {}

local REC_SIZE = 0x90        -- 144 bytes
local MAX_HITS = 300

-- Fire-mode fingerprint: mode array holds single(2)+burst(3) (either order),
-- the third mode slot is none(0), and TertiaryFireMode (+0x7C) is none(0).
local function examine(window_base, window)
    local limit = #window - 0x80
    for off = 0, limit, 4 do
        local m0 = u32_at(window, off + 0x70 + 1)
        local m1 = u32_at(window, off + 0x74 + 1)
        local m2 = u32_at(window, off + 0x78 + 1)
        local m3 = u32_at(window, off + 0x7C + 1)
        if m0 and m1 and m2 and m3 then
            local semi_burst = (m0 == 2 and m1 == 3) or (m0 == 3 and m1 == 2)
            if semi_burst and m2 == 0 and m3 == 0 then
                local abs = window_base + off
                if not seen[abs] and #hits < MAX_HITS then
                    seen[abs] = true
                    local rec = read_at(abs, REC_SIZE)
                    if rec then
                        hits[#hits + 1] = { addr = abs, rec = rec }
                        log(string.format("hit %d @ 0x%X: mode [%d,%d,%d,%d] +0 f32=%.1f +4 f32=%.1f",
                            #hits, abs, m0, m1, m2, m3,
                            f32_at(rec, 1) or -1, f32_at(rec, 5) or -1))
                    end
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

local function dump_all()
    local lines = {}
    lines[#lines + 1] = string.format("fmscan: %d fire-mode candidate records (fingerprint [single+burst, none, none])", #hits)
    for i, h in ipairs(hits) do
        lines[#lines + 1] = string.format("--- hit %d @ 0x%X | mode [%d,%d,%d,%d] | +0 f32=%.1f +4 f32=%.1f ---",
            i, h.addr,
            u32_at(h.rec, 0x70 + 1), u32_at(h.rec, 0x74 + 1), u32_at(h.rec, 0x78 + 1), u32_at(h.rec, 0x7C + 1),
            f32_at(h.rec, 1) or -1, f32_at(h.rec, 5) or -1)
        lines[#lines + 1] = hexdump(h.rec)
    end
    if out_dir then
        local ok, f = pcall(io.open, out_dir .. "/fmscan_records.txt", "w")
        if ok and f then pcall(f.write, f, table.concat(lines, NL) .. NL); pcall(f.close, f) end
    end
    log(string.format("dumped %d records to fmscan_records.txt", #hits))
end

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
            else
                local ok, err = pcall(dump_all)
                if not ok then log("dump error: " .. tostring(err)) end
                state.phase = "done"
            end
        end
        return original_update(...)
    end
    log("fmscan loaded; value-scanning for the fire-mode record")
    state.phase = "scanning"
end

return { revision = REVISION, state = state }
