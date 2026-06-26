import argparse, json

def calculate(seat_size, total_seats, finance_staff, has_manager_office,
              meeting_area, reception_area, pantry_area, finance_area,
              manager_office_area=12.0):
    if has_manager_office:
        effective_seats = total_seats - finance_staff - 1
        manager_count = 1
    else:
        effective_seats = total_seats - finance_staff
        manager_count = 0

    net_workstation = effective_seats * seat_size
    workstation_with_aisles = net_workstation / 0.65

    subtotal = workstation_with_aisles + meeting_area + reception_area + pantry_area + finance_area
    if has_manager_office:
        subtotal += manager_office_area

    total_area = round(subtotal / 0.65, 1)

    return {
        'total_area_sqm': total_area,
        'recommended_area_with_buffer_sqm': round(total_area * 1.10, 1),
        'net_workstation_sqm': round(net_workstation, 2),
        'workstation_with_aisles_sqm': round(workstation_with_aisles, 2),
        'functional_subtotal_sqm': round(subtotal, 2),
        'details': {
            'total_seats': total_seats,
            'finance_staff': finance_staff,
            'has_manager_office': has_manager_office,
            'effective_workstation_seats': effective_seats,
            'manager_count': manager_count,
            'manager_office_area_sqm': manager_office_area if has_manager_office else 0,
            'seat_size_sqm': seat_size,
            'seat_dimensions': '1.2x1.2m' if seat_size == 1.44 else '1.4x1.4m',
            'meeting_area_sqm': meeting_area,
            'reception_area_sqm': reception_area,
            'pantry_area_sqm': pantry_area,
            'finance_room_area_sqm': finance_area,
        }
    }

def main():
    p = argparse.ArgumentParser(description='Office Area Calculator (Zhide Laoshi 20 yrs)')
    p.add_argument('--seats', type=int, required=True)
    p.add_argument('--finance', type=int, default=0)
    p.add_argument('--seat-size', type=float, required=True)
    p.add_argument('--meeting', type=float, default=0)
    p.add_argument('--reception', type=float, default=0)
    p.add_argument('--pantry', type=float, default=0)
    p.add_argument('--finance-room', type=float, default=0)
    p.add_argument('--has-manager-office', action='store_true',
                   help='Include manager private office (reduces workstation count by 1, adds office area)')
    p.add_argument('--manager-area', type=float, default=12.0,
                   help='Manager office area in sqm (default: 12.0, range: 12-15)')
    p.add_argument('--json', action='store_true')
    args = p.parse_args()

    r = calculate(args.seat_size, args.seats, args.finance, args.has_manager_office,
                  args.meeting, args.reception, args.pantry, args.finance_room,
                  args.manager_area)

    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2)); return

    d = r['details']
    print()
    print('=' * 46)
    print('       Office Area Calculator')
    print('   (by Zhide Laoshi, 20 yrs experience)')
    print('=' * 46)
    print(f'  Total seats      : {d["total_seats"]} persons')
    print(f'  Finance staff    : {d["finance_staff"]} persons')
    print(f'  Manager office   : {"Yes - " + str(d["manager_office_area_sqm"]) + " sqm" if d["has_manager_office"] else "No"}')
    print(f'  Effective seats  : {d["effective_workstation_seats"]} persons')
    print(f'  Seat size        : {d["seat_dimensions"]} ({d["seat_size_sqm"]} sqm)')
    print()
    print('  Functional areas :')
    print(f'    Meeting room   : {d["meeting_area_sqm"]} sqm')
    print(f'    Reception      : {d["reception_area_sqm"]} sqm')
    print(f'    Pantry         : {d["pantry_area_sqm"]} sqm')
    print(f'    Finance room   : {d["finance_room_area_sqm"]} sqm')
    if d["has_manager_office"]:
        print(f'    Manager office : {d["manager_office_area_sqm"]} sqm')
    print()
    print('-' * 46)
    print(f'  Net workstation  : {r["net_workstation_sqm"]} sqm')
    print(f'  + Aisle factor   : {r["workstation_with_aisles_sqm"]} sqm')
    print(f'  Subtotal         : {r["functional_subtotal_sqm"]} sqm')
    print('-' * 46)
    print(f'  RECOMMENDED TOTAL: {r["total_area_sqm"]} sqm')
    print(f'  +10%% buffer      : {r["recommended_area_with_buffer_sqm"]} sqm')
    print('=' * 46)
    print()
    print('  Note: Excludes elevators, restrooms, public areas.')
    print('  Add 10-15%% buffer when selecting actual location.')

if __name__ == '__main__':
    main()
