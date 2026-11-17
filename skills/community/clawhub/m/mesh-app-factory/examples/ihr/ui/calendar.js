export default {
inject:['service', 'tags'],
data() {return {
    cals:[],
    days:[],
    cal:0, //当前日历id
    edt:{cal:{name:''}},
    ctrl:{no:-2,tag:'',calDlg:false,year:2000,month:1,
         start:0,end:0,firstDay:0},
}},
created(){
    this.query_cals();
    var dt=new Date();
    var year=dt.getFullYear();
    this.ctrl.year=year;
    this.ctrl.month=dt.getMonth()+1;
},
methods:{
query_cals(){
    var opts={method:"GET", url:"/config/listCalendar"}
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            return;
        }
        this.cals=resp.data.list.map(c => {
            return {label:c.name, value:c.id}
        });
        this.cal=this.cals[0].value;
        this.query_days();
    })  
},
query_days(){
    var mon=this.ctrl.year+this.ctrl.month.toString().padStart(2,'0');
    var start=mon+'01';
    this.start=start;
    // 给定月份下一个月的0天就是当前月的最后一天，month是从1开始的
    var dt=new Date(this.ctrl.year,this.ctrl.month,0);
    var lastDay=dt.getDate();
    var end=mon+lastDay.toString().padStart(2,'0');
    this.end=end;
    var opts={method:"GET", url:"/config/queryCalendar?calendar="
        +this.cal+"&start="+start+"&end="+end};
    dt=new Date(this.ctrl.year,this.ctrl.month-1,1);
    var firstDay=dt.getDay();//1号是星期几，0-6
    this.firstDay=firstDay; //0-6;
    var dayNum=firstDay+lastDay; //可见的天数
    if(dayNum % 7 > 0) {
        dayNum += (7 - dayNum%7);
    }
    end=firstDay+lastDay;
    request(opts, this.service.name).then(resp => {
        var n = 1;
        var s = '';
        var days=[];
        for(var i=0;i<dayNum;i+=7) {
            var w=[];
            for(var j=i;j<i+7;j++) {//每7天一行
                s= (j < this.firstDay || j >= end)?'':(n++);
                w.push({d:s,t:'text-center',c:''});
            }
            days.push(w);
        }
        if(resp.code==RetCode.OK) {
            var dd=resp.data.list;
            var cls;
            var day;
            for(var d of dd) {
                day=d.d-this.start+1;
                n = day+firstDay-1;
                if(d.t=='F')cls='text-center bg-green';
                else if(d.t=='O')cls='text-center bg-teal';
                else cls='text-center';
                days[parseInt(n/7)][n%7]={d:day, t:d.t, cls:cls, c:d.c, d1:d.d};
            }
        }
        this.days=days;
    });
},
show_cal(i) {
    if(i>-1) {
        this.ctrl.tag=this.tags.modify;
        var no;
        for(var i in this.cals) {
            if(this.cals[i].value==this.cal) {
                no=i;
                break;
            }
        }
        this.ctrl.no=no;
        this.edt.cal.id=this.cals[no].value;
        this.edt.cal.name=this.cals[no].label;
    } else {
        this.ctrl.tag=this.tags.add;
        this.edt.cal.name='';
        this.ctrl.no=i;
    }
    this.ctrl.tag+=this.tags.cfg.calendar;
    this.ctrl.calDlg=true;
},
cal_do() {
    var opts;
    if(this.ctrl.no>-1) {
        opts={method:"PUT",url:"/config/setCalendar",data:this.edt.cal};
    } else {
        opts={method:"POST",url:"/config/addCalendar",data:this.edt.cal};
    }
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        if(this.ctrl.no>-1) {
            this.cals[this.ctrl.no].label=this.edt.cal.name;
        } else {
            var opt = {value:resp.data.id,label:this.edt.cal.name};
            this.cals.push(opt);
        }
        this.ctrl.no=-2;
        this.ctrl.calDlg=false;
    });
},
remove_cal() {
    if(this.cals.length==1) {
        return;
    }
    var opts={method:"DELETE",url:"/config/removeCalendar?id="+this.cal};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        var no;
        for(var i in this.cals) {
            if(this.cals[i].value==this.cal) {
                no=i;
                break;
            }
        }
        this.cals.splice(no,1);
        this.cal = this.cals[0].value;
        this.query_days();
    });
},
set_month(ym) {
    this.ctrl.year=ym.year;
    this.ctrl.month=ym.month; //不减1
    this.query_days();
},
init_cal(){
    var opts={method:"POST",url:"/config/initCalendarDays",
         data:{calendar:this.cal,start:this.start,end:this.end}};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.query_days();
    });
},
set_day(d) {
    var n=d-this.start+this.firstDay;
    var r=parseInt(n/7);
    var c=n%7;
    var day=this.days[r][c];
    var type;
    //轮流转变
    if(day.t=='W')type='O';
    else if(day.t=='O')type='F';
    else type='W';
    
    var opts={method:"PUT",url:"/config/setCalendarDay",
         data:{calendar:this.cal,day:d,type:type,cmt:''}};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        var cls;
        if(type=='F')cls='text-center bg-green';
        else if(type=='O')cls='text-center bg-teal';
        else cls='text-center';
        day.cls=cls;
        day.t=type;
    });    
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat round icon="arrow_back" dense @click="service.back()"></q-btn>
     <q-toolbar-title>{{tags.cfg.calendar}}</q-toolbar-title>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">
<div>
<q-select v-model="cal" :options="cals" @update:model-value="query_days"
dense map-options emit-value ref="calSelect">
 <template v-slot:after>
  <q-btn flat dense color="primary" icon="add_circle" @click="show_cal(-1)"></q-btn>
  <q-btn flat dense color="primary" icon="edit" @click="show_cal(1)"></q-btn>
  <q-btn flat dense color="red" icon="cancel" @click="remove_cal()" v-if="cals.length>1"></q-btn>
 </template>
</q-select>
</div>
<div class="row justify-start">
  <div class="col self-center">
   <month-input class="text-subtitle1" @update:modelValue="set_month" min="-10" max="+5"></month-input>
  </div>
  <div class="col self-center">
   <q-btn flat dense color="teal" icon="event_repeat"
   @click="init_cal" class="q-pl-lg" :label="tags.initCal"></q-btn>
  </div>
</div>
<div class="q-pa-none">
<q-markup-table separator="cell" flat bordered>
 <thead>
   <tr><th class="text-center" v-for="d in tags.weekDays">{{d}}</th></tr>
 </thead>
 <tbody>
   <tr v-for="w in days">
     <td v-for="d in w" :class="d.cls" @click="set_day(d.d1)">{{d.d}}</td>
   </tr>
 </tbody>
</q-markup-table>
</div>
<q-separator spaced></q-separator>
<div class="row justify-end">
 <q-badge color="white" text-color="black">{{tags.cfg.workDay}}<q-icon name="engineering"></q-icon></q-badge>
 <q-badge color="teal">{{tags.cfg.offDay}}<q-icon name="coffee"></q-icon></q-badge>
 <q-badge color="green">{{tags.cfg.festival}}<q-icon name="festival"></q-icon></q-badge>
</div>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="ctrl.calDlg">
 <q-card style="min-width:70vw">
  <q-card-section>
    <div class="text-h6">{{ctrl.tag}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-input :label="tags.name" v-model="edt.cal.name" dense></q-input>
  </q-card-section>
  <q-card-actions align="right">
   <q-btn :label="tags.ok" color="primary" @click="cal_do"></q-btn>
   <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
`
}