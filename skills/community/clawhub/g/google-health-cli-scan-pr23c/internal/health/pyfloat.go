package health

import (
	"math"
	"strconv"
	"strings"
)

// pyFloat is a float64 that marshals to JSON the way CPython's repr(float) /
// json.dumps does, rather than the way Go's encoding/json does. The difference
// is load-bearing for byte-fidelity: Python always renders a float with a
// decimal point ("134.0", not Go's "134") while keeping the same shortest
// digits (GOAL.md §11, §15). Heart rate / calories are integers in all real
// data, so pyFloat only matters for the rare fractional value — but matching it
// keeps `sessions --json` byte-identical regardless (ported from
// speediance-cli-go: internal/template/pyfloat.go).
type pyFloat float64

// MarshalJSON renders the value via pyFloatRepr, producing a valid JSON number.
func (p pyFloat) MarshalJSON() ([]byte, error) {
	return []byte(pyFloatRepr(float64(p))), nil
}

// pyFloatRepr reproduces CPython's float repr (shortest round-tripping digits,
// fixed vs. scientific chosen by the same decpt thresholds, and an appended
// ".0" for integral values). Go and Python both compute the same shortest digit
// string for a given float64, so only the placement/formatting needs matching.
func pyFloatRepr(f float64) string {
	switch {
	case math.IsInf(f, 1):
		return "1e999"
	case math.IsInf(f, -1):
		return "-1e999"
	case math.IsNaN(f):
		return "0"
	case f == 0:
		if math.Signbit(f) {
			return "-0.0"
		}
		return "0.0"
	}

	neg := math.Signbit(f)
	sci := strconv.FormatFloat(f, 'e', -1, 64)
	if neg {
		sci = sci[1:]
	}

	eIdx := strings.IndexByte(sci, 'e')
	mant := sci[:eIdx]
	exp, _ := strconv.Atoi(sci[eIdx+1:])

	digits := mant
	if dot := strings.IndexByte(mant, '.'); dot >= 0 {
		digits = mant[:dot] + mant[dot+1:]
	}
	nd := len(digits)
	decpt := exp + 1

	var out string
	switch {
	case decpt <= -4 || decpt > 16:
		m := digits[:1]
		if nd > 1 {
			m += "." + digits[1:]
		}
		e := decpt - 1
		sign := "+"
		if e < 0 {
			sign = "-"
			e = -e
		}
		es := strconv.Itoa(e)
		if len(es) < 2 {
			es = "0" + es
		}
		out = m + "e" + sign + es
	case decpt <= 0:
		out = "0." + strings.Repeat("0", -decpt) + digits
	case decpt >= nd:
		out = digits + strings.Repeat("0", decpt-nd) + ".0"
	default:
		out = digits[:decpt] + "." + digits[decpt:]
	}
	if neg {
		out = "-" + out
	}
	return out
}
