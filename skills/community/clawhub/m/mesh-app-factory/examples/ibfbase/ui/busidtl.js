import AlertDialog from "/assets/v3/components/alert_dialog.js";
import ConfirmDialog from "/assets/v3/components/confirm_dialog.js";
import DatetimeInput from "/assets/v3/components/datetime_input.js"
import {datetimeToDate, datetimeToStr} from '/assets/v3/components/datetime_input.js';
import {addrToStr} from '/assets/v3/components/addr_input.js';
import {sta2icon} from '/assets/v3/components/workflow.js';
import AddrInput from "/assets/v3/components/addr_input.js";
import PrjInput from "./components/prj_selector.js";

const EMPTY_EXP={start_s:'',end_s:'',val:'',invoice:'',cmt:''};
export default {
inject:["ibf"],
components:{
    "alert-dialog":AlertDialog,
    "confirm-dialog":ConfirmDialog,
    "datetime-input":DatetimeInput,
    "addr-input":AddrInput,
    "prj-input":PrjInput
},
data() {return {
    id:this.$route.query.id,
    tags:this.ibf.tags,
    editable:true,
    editing:false,
    dtl:{},
    edtDtl:{},
    expList:[], //报销列表
    expAct:{dlg:false,dta:{},no:-1}
}},
created(){
    this.query_dtl();
},
methods:{
query_dtl() {
    var url="/business/detail?id="+this.id;
    request({method:"GET", url:url}, this.ibf.SERVICE_BUSINESS).then(resp => {
        if(resp.code!=RetCode.OK) {
            return;
        }
        var dt=new Date();
        //start,end,val,invoice,cmt
        if(resp.data.expenses) {
            this.expList=resp.data.expenses.map(b=>{
                dt.setTime(b.start*60000);
                b.start_s=datetime2str(dt);
                dt.setTime(b.end*60000);
                b.end_s=datetime2str(dt);
                return b;
            });
        } else {
            this.expList=[];
        }
        //pid,prjName,start,end,subsidy,expense,uid,account
        //status,overAt,dest,reason,cmt,flowid,power
        //account,cfmAcc,cfmAt,dest,reason,cmt
        var b=resp.data;
        if(b.overAt>0) {
            dt.setTime(b.overAt*60000);
            b.overAt=date2str(dt);
        } else {
            b.overAt=this.tags.notOver;
        }
        dt.setTime(b.start*60000);
        b.start_s=datetime2str(dt);
        dt.setTime(b.end*60000);
        b.end_s=datetime2str(dt);
        b.staIcon=sta2icon(b.status);
        delete b.expenses;
        this.dtl=b;
        this.editable=b.status!=100&&b.uid==this.ibf.userInfo.id;
    })
},
show_exp(no) {
    this.expAct.dlg=true;
    this.expAct.no=no;
    if(no>-1) {
        copyObjTo(this.expList[no],this.expAct.dta);
    } else {
        copyObjTo(EMPTY_EXP,this.expAct.dta);
    }
},
exp_do() {
    var dta=copyObj(this.expAct.dta,["val","cmt","invoice"]);
    dta.start=parseInt(datetimeToDate(this.expAct.dta.start_s).getTime()/60000);
    dta.end=parseInt(datetimeToDate(this.expAct.dta.end_s).getTime()/60000);
    dta.business=this.id;
    if(dta.start<this.dtl.start) {
        this.$refs.alertDlg.show(this.tags.notInBusiTime);
        return;
    }
    if(dta.end>this.dtl.end) {
        this.$refs.alertDlg.show(this.tags.notInBusiTime);
        return;
    }
    var opts;
    if(this.expAct.no>-1) { //修改
        opts={method:"PUT", url:"/expense/update", data:dta};
    } else {
        opts={method:"POST", url:"/expense/add", data:dta};
    }
    request(opts, this.ibf.SERVICE_BUSINESS).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.expAct.dlg=false;
        this.expAct.no=-1;
        this.query_dtl();
    });
},
remove_exp() {
    if(this.expAct.no<0)return;
    var invoice=this.expAct.dta.invoice;
    var url="/expense/remove?business="+this.id+"&invoice="+invoice;
    request({method:"DELETE",url:url}, this.ibf.SERVICE_BUSINESS).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.expAct.dlg=false;
        this.expAct.no=-1;
        this.query_dtl();
    });
},
cal_subsidy() {
    var url="/employee/subsidy";
    request({method:"GET",url:url}, this.ibf.SERVICE_HR).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        var dayNum= Math.floor((this.dtl.end-this.dtl.start) / 1440);
        this.edtDtl.subsidy=resp.data.subsidy*dayNum;
    });
},
show_edit() {
    this.editing=true;
    copyObjTo(this.dtl, this.edtDtl);
},
update_busi() {
    var dta=copyObj(this.edtDtl,['subsidy','dest','reason','cmt']);
    dta.id=this.id;
    dta.start=parseInt(datetimeToDate(this.edtDtl.start_s).getTime()/60000);
    dta.end=parseInt(datetimeToDate(this.edtDtl.end_s).getTime()/60000);
    if(typeof(this.edtDtl.dest)==='string') {
        dta.dest=this.edtDtl.dest;
    } else {
        dta.dest=addrToStr(this.edtDtl.dest);
    }
    request({method:"PUT", url:"/business/update", data:dta}, this.ibf.SERVICE_BUSINESS).then(resp=>{
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.editing=false;
        copyObjTo(this.edtDtl, this.dtl);
        this.dtl.start_s=datetimeToStr(this.edtDtl.start_s,this.tags.dateFmt);
        this.dtl.end_s=datetimeToStr(this.edtDtl.end_s,this.tags.dateFmt);
        this.dtl.dest=addrToStr(this.edtDtl.dest);
    });
},
remove_busi() {
    this.$refs.cfmDlg.show(this.tags.cfmRmv, ()=>{
        var opts={method:"DELETE",url:"/business/remove?id="+this.id};
        request(opts, this.ibf.SERVICE_BUSINESS).then(resp => {
            if(resp.code!=RetCode.OK) {
                this.$refs.alertDlg.showErr(resp.code, resp.info);
                return;
            }
            this.ibf.back();
        })
    });
},
busi_flow() {
    var url='/ibf/workflow?flow='+this.dtl.flowid+"&did="+this.id
        +"&flName=busi&service="+this.ibf.SERVICE_BUSINESS+"&step="+this.dtl.status
        +"&dtlApi=" + encodeURI('/business/detail');
    this.ibf.goto(url);
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat icon="arrow_back" dense @click="ibf.back()"></q-btn>
     <q-toolbar-title>{{tags.busi.title}}-{{dtl.prjName}}</q-toolbar-title>
     <q-btn flat icon="clear" @click="remove_busi()" v-if="editable" dense></q-btn>
     <q-btn flat icon="edit" @click="show_edit" v-if="editable&&!editing" dense></q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-sm">
<q-list dense v-if="!editing">
  <q-item>
    <q-item-section>{{tags.start}}</q-item-section>
    <q-item-section side>{{dtl.start_s}}</q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.end}}</q-item-section>
    <q-item-section side>{{dtl.end_s}}</q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.busi.dest}}</q-item-section>
    <q-item-section side>{{dtl.dest}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.busi.subsidy}}</q-item-section>
   <q-item-section side>{{dtl.subsidy}}</q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.busi.expense}}</q-item-section>
    <q-item-section side>{{dtl.expense}}</q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.busi.overAt}}</q-item-section>
    <q-item-section side>{{dtl.overAt}}</q-item-section>
  </q-item>
  <q-item clickable @click.stop="busi_flow">
    <q-item-section>{{tags.busi.status}}</q-item-section>
    <q-item-section side><q-icon :name="dtl.staIcon" color="blue"></q-icon></q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.busi.reason}}</q-item-section>
    <q-item-section side>{{dtl.reason}}</q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.cmt}}</q-item-section>
    <q-item-section side>{{dtl.cmt}}</q-item-section>
  </q-item>
</q-list>
<div v-else>
  <datetime-input v-model="edtDtl.start_s" :label="tags.start"
  :format="tags.dateFmt" :showMinute="false"></datetime-input>
  <datetime-input v-model="edtDtl.end_s" :label="tags.end"
   :format="tags.dateFmt" :showMinute="false"></datetime-input>
  <addr-input v-model="edtDtl.dest" :label="tags.busi.dest"></addr-input>
  <q-input v-model.number="edtDtl.subsidy" :label="tags.busi.subsidy">
   <template v-slot:append>
     <q-icon name="calculate" color="primary" @click="cal_subsidy"></q-icon>
   </template>
  </q-input>
  <q-input v-model="edtDtl.reason" :label="tags.busi.reason" type="textarea" rows="2"></q-input>
  <q-input v-model="edtDtl.cmt" :label="tags.cmt" type="textarea" rows="2"></q-input>
  <div class="row justify-end q-py-md">
    <div class="col-2">
      <q-btn flat :label="tags.cancel" @click="editing=false" color="primary"></q-btn>
    </div>
    <div class="col-2">
      <q-btn :label="tags.ok" @click="update_busi" color="primary"></q-btn>
    </div>
  </div>
</div>
<q-banner inline-actions dense class="bg-indigo-3 text-white">
  {{tags.busi.expense}}
  <template v-slot:action>
    <q-btn icon="add_circle" @click="show_exp(-1)" flat dense></q-btn>
  </template>
</q-banner>
<q-list dense separator>
  <q-item v-for="(e,i) in expList" :clickable="editable" @click="show_exp(i)">
    <q-item-section>
     <q-item-label>{{e.invoice}}</q-item-label>
     <q-item-label caption>{{e.cmt}}</q-item-label>
    </q-item-section>
    <q-item-section side>
     <q-item-label>{{e.val}}</q-item-label>
     <q-item-label caption>{{e.start_s}}-&gt;{{e.end_s}}</q-item-label>
    </q-item-section>
  </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs"
 ref="alertDlg"></alert-dialog>
<confirm-dialog :title="tags.attention" :ok="tags.ok"
 :close="tags.cancel" ref="cfmDlg"></confirm-dialog>

<q-dialog v-model="expAct.dlg">
 <q-card style="min-width:70vw">
  <q-card-section>
   <div class="text-h6">{{tags.busi.expense}}</div>
   <q-separator></q-separator>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <div class="row">
    <div class="col">
     <datetime-input v-model="expAct.dta.start_s" :label="tags.start"
      :format="tags.dateFmt" :showMinute="false"></datetime-input>
    </div>
    <div class="col-2 self-center text-center">
     <q-icon name="arrow_right_alt" size="2em"></q-icon>
    </div>
    <div class="col">
     <datetime-input v-model="expAct.dta.end_s" :label="tags.end"
     :format="tags.dateFmt" :showMinute="false"></datetime-input>
    </div>
   </div>
   <div>
    <q-input v-model.number="expAct.dta.val" :label="tags.busi.val"></q-input>
    <q-input v-model="expAct.dta.invoice" :label="tags.busi.invoice"></q-input>
    <q-input v-model="expAct.dta.cmt" :label="tags.cmt"></q-input>
   </div>
  </q-card-section>
  <q-card-actions align="right">
    <q-btn flat :label="tags.remove" color="red" @click="remove_exp" v-show="expAct.no>-1"></q-btn>
    <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    <q-btn :label="tags.ok" color="primary" @click="exp_do"></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>
`
}