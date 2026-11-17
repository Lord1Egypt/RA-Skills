import AlertDialog from "/assets/v3/components/alert_dialog.js"
import Language from "./language.js"

const l=Platform.language();
const tags = l.indexOf("zh") == 0 ? Language.zh : Language.en;
function registerIbf(app, router, service) { //注册ibf所需的路由
    router.addRoute({path:"/ibf/department", component:()=>import('./department.js')});
    router.addRoute({path:"/ibf/my", component:()=>import('./my.js')});
    router.addRoute({path:"/ibf/resume", component:()=>import('./resume.js')});
    router.addRoute({path:"/ibf/contacts", component:()=>import('./contacts.js')});
    router.addRoute({path:"/ibf/prjproc", component:()=>import('./prjproc.js')}); //项目事务流程
    router.addRoute({path:"/ibf/purchasedtl", component:()=>import('./purchasedtl.js')}); //项目采购申请，接口在iresource中实现
    router.addRoute({path:"/ibf/setprice", component:()=>import('./setprice.js')}); //采购员设置采购单价
    router.addRoute({path:"/ibf/prjinfo", component:()=>import('./prjinfo.js')}); //项目状态信息
    router.addRoute({path:"/ibf/attendance", component:()=>import('./attendance.js')}); //考勤
    router.addRoute({path:"/ibf/business", component:()=>import('./business.js')}); //差旅列表
    router.addRoute({path:"/ibf/busidtl", component:()=>import('./busidtl.js')}); //差旅详情
    router.addRoute({path:"/ibf/workflow", component:()=>import('./workflow.js')}); //工作流
    router.addRoute({path:"/ibf/tasks", component:()=>import('./tasks.js')}); //待办
    router.addRoute({path:"/ibf/settings", component:()=>import('./settings.js')}); //工作流、配置、定时任务的配置
    const ibfDta = {
        tags:tags,
        lang:l, //语言
        service:service, //所处服务名称
        userInfo:{id:-1,powers:{}},
        prjs:[],
        runtime:{}, //运行时
        tmpl:{},//扩展字段模板
        department:{}, //所属部门，作为普通员工，只能从属于一个部门
        adminDpms:[], //管理的部门
        clockTms:[],
        SERVICE_HR:"ihr",
        SERVICE_WF:"workflow",
        SERVICE_CRM:"icrm",
        SERVICE_FINANCE:"ifinance",
        SERVICE_BUSINESS:"ibusiness",
        SERVICE_PRJ:"iproject",
        SERVICE_RES:"iresource",
        N_PAGE:10,
        N_SMPG:5,
        CLIENTW:document.documentElement.clientWidth,
        PrjStage:{init:'INIT',start:'START',end:'END',cancel:'CANC'},
        PlanState:{init:'INIT',norm:'NORM',adv:'ADVA',delay:'DELA',cancel:'CANC'},
        back(){router.back()},
        goto(url){router.push(url)},
        setRt(k,v) {
            this.runtime[router.currentRoute.value.path+':'+k]=v;
        },
        getRt(k,def) {
            var v=this.runtime[router.currentRoute.value.path+':'+k];
            return v?v:def;
        },
        showFlow(flowid,did,url) {
            this.goto(appendParas(url,{flow:flowid,did:did}));
        },
        template(n,url,def){
            var k=this.service+'.'+n;
            var tmpl=this.tmpl[k];
            if(tmpl&&Object.keys(tmpl).length>0){
                return new Promise(resolve=>{resolve(tmpl)});
            }
            return request({method:"GET",url:url}, this.service).then((resp)=>{
                if(resp.code!=RetCode.OK || !resp.data || !resp.data.v) {
                    Console.info("request template `"+k+"` failed:"+resp.code+",info:"+resp.info);
                    return def;//返回默认值
                }
                if(resp.data.v) {
                    this.tmpl[k]=JSON.parse(resp.data.v);
                }
                 return this.tmpl[k]?this.tmpl[k]:def;
            })
        }
    };
    app.provide('ibf', ibfDta);

    //返回userInfo
    return request({method:"GET",url:"/api/getbaseinfo"}, SERVICE_USER).then(resp=>{
        if(resp.code!=0) {
            console.info("request failed:" + resp.code + ",info:" + resp.info);
            return {id:-1,powers:{},groups:[]};
        }
        if(!resp.data.powers)resp.data.powers={}; //防止引用时powers为空
        if(!resp.data.groups)resp.data.groups=[];
        ibfDta.userInfo=resp.data;
        return ibfDta.userInfo;
    })
}
export { registerIbf };

export default {
inject:['ibf'],
components: {
    "alert-dialog" : AlertDialog
},
data() {return {
    tags:tags,
    ctrl:{cur:1, max:0},
    prjs:[],//vue无法与inject的变量双向绑定，所以另外加以下三个字段
    isAdmin:false,
    clockTms:[],
    taskNum:0
}},
created(){
    if(this.ibf.prjs.length==0) {
        this.query_prjs(1);
    } else {
        this.prjs=this.ibf.prjs;
        this.ctrl=this.ibf.ctrl;
    }
    if(this.ibf.clockTms.length==0) {
        request({method:"GET",url:"/attendance/clockAt"}, this.ibf.SERVICE_HR).then(resp=>{
            if(resp.code!=RetCode.OK) {
                this.set_clockTms([]);
                return;
            }
            this.set_clockTms(resp.data.clockTimes);
        });
    } else {
        this.clockTms=this.ibf.clockTms;
    }
    if(!this.ibf.department.role&&this.ibf.adminDpms.length==0) {
        var opts={method:"GET",url:"/grp/myDepartment"};
        request(opts, this.ibf.SERVICE_HR).then(resp => {
            var adms=[];
            var dep={};
            if(resp.code==RetCode.OK) {
                for(var d of resp.data.list) {
                    if(d.role=='ADM') {
                        d.adm=true;
                        adms.push(d);
                    } else {
                        dep=d;
                    }
                }
            }
            this.isAdmin=adms.length>0;
            this.ibf.department=dep;
            this.ibf.adminDpms=adms;
        });
    } else {
        this.isAdmin=this.ibf.adminDpms.length>0;
    }
    
    request({method:"GET",url:"/taskNum"}, this.ibf.SERVICE_WF).then(resp => {
        if(resp.code==RetCode.OK) {
            this.taskNum=resp.data.num
        }
    })
},
methods:{
query_prjs(pg) {
    var pgSize=this.ibf.N_PAGE;
    var offset=(parseInt(pg)-1)*pgSize;
    var url='/project/my?offset='+offset+'&num='+pgSize;
    request({method:"GET", url:url}, this.ibf.SERVICE_PRJ).then(resp=>{
        var prjs=[];
        if(resp.code!=RetCode.OK) {
            this.ctrl.max=0;
            this.ctrl.cur=1;
        } else {
            var tm,stage;
            var dt=new Date();
            var prjTags=this.tags.prj;
            for(var l of resp.data.list) {
                dt.setTime(l.start*60000);
                tm=date2str(dt);
                dt.setTime(l.end*60000);
                tm+='--'+date2str(dt);
                l.time=tm;
                stage=prjTags.stageCfg[l.stage];
                if(stage) {
                    l.stage=stage;
                }
                l.role=prjTags.roleCfg[l.role];
                l.type=prjTags.typeCfg[l.type];
                prjs.push(l);
            }
            this.ibf.prjNum=resp.data.total;
            this.ctrl.max=Math.ceil(resp.data.total/pgSize);
        }
        this.ibf.prjs=prjs;
        this.ibf.ctrl=this.ctrl; //回退时使用历史记录
        this.prjs=prjs;
    });
},
set_clockTms(tms) {
    var dt=new Date();
    var clkTms=[];
    var start,end;
    var m, h;
    for(var tm of tms) {
        dt.setTime(tm.start*60000);
        h=dt.getHours();
        m=dt.getMinutes();
        start=(h<10?'0'+h:h)+':'+(m<10?'0'+m:m);

        dt.setTime(tm.end*60000);
        h=dt.getHours();
        m=dt.getMinutes();
        end=(h<10?'0'+h:h)+':'+(m<10?'0'+m:m);
        clkTms.push({start:start,end:end});
    }
    if(clkTms.length==0) {
        clkTms=[{start:'00:00',end:'00:00'}]
    }
    this.clockTms=clkTms;
    this.ibf.clockTms=clkTms;
},
clock() { //上下班刷卡
    request({method:"GET",url:"/attendance/clock"}, this.ibf.SERVICE_HR).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.set_clockTms([{start:resp.data.start, end:resp.data.end}]);
    })
}
},
template:`
<div class="row">
 <div class="col-1 self-center">
  <q-btn color="deep-orange" no-caps @click="clock" style="min-width:28vw">
   <div class="row items-center no-wrap">
    <q-icon left name="event_available"></q-icon>
    <div class="text-center">
     <div class="text-h5">{{tags.home.attendance}}</div>
     <div v-for="c in clockTms">{{c.start}}-{{c.end}}</div>
    </div>
   </div>
  </q-btn>
 </div>
 <div class="col self-center text-right">
  <div class="q-gutter-lg">
   <q-btn flat dense color="primary" @click="ibf.goto('/ibf/tasks')">
    <div class="text-center">
     <q-btn icon="assignment" flat dense>
     <q-badge v-if="taskNum>0" color="red" rounded floating>{{taskNum}}</q-badge>
     </q-btn><br>
     {{tags.home.tasks}}
    </div>
   </q-btn>
   <q-btn flat dense color="primary" @click="ibf.goto('/ibf/attendance')">
    <div class="text-center">
     <q-btn icon="work_history" flat dense></q-btn><br>
     {{tags.atd.title}}
    </div>
   </q-btn>
   <q-btn flat dense color="primary" @click="ibf.goto('/ibf/business')">
    <div class="text-center">
     <q-btn icon="flight_takeoff" flat dense></q-btn><br>
     {{tags.busi.title}}
    </div>
   </q-btn>
   <q-btn flat dense color="primary" @click="ibf.goto('/ibf/contacts')">
    <div class="text-center">
     <q-btn icon="person_search" flat dense></q-btn><br>
     {{tags.contacts.title}}
    </div>
   </q-btn>
   <q-btn flat dense color="primary" @click="ibf.goto('/ibf/my')">
    <div class="text-center">
     <q-btn icon="sensor_occupied" flat dense></q-btn><br>
     {{tags.my.title}}
    </div>
   </q-btn>
   <q-btn flat dense color="primary" @click="ibf.goto('/ibf/department')" v-if="isAdmin">
    <div class="text-center">
     <q-btn icon="group" flat dense></q-btn><br>
     {{tags.grp.department}}
    </div>
   </q-btn>
   <q-btn flat dense color="teal" @click="ibf.goto('/ibf/settings')" v-if="ibf.userInfo.account=='admin'">
    <div class="text-center">
     <q-btn icon="settings" flat dense></q-btn><br>
     {{tags.home.settings}}
    </div>
   </q-btn>
  </div>
 </div>
</div>
<q-separator spaced="md"></q-separator>
<q-list dense separator>
  <q-item v-for="p in prjs" clickable @click="ibf.goto('/ibf/prjproc?id='+p.id)">
   <q-item-section>
    <q-item-label>{{p.name}}</q-item-label>
    <q-item-label caption>{{p.role}}</q-item-label>
   </q-item-section>
   <q-item-section>
    <q-item-label>{{p.stage}}</q-item-label>
    <q-item-label caption>{{p.time}}</q-item-label>
   </q-item-section>
   <q-item-section side>{{p.type}}</q-item-section>
  </q-item>
</q-list>
<div class="q-pa-sm flex flex-center" v-show="ctrl.max>1">
 <q-pagination v-model="ctrl.cur" color="primary" :max="ctrl.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query_prjs"></q-pagination>
</div>
<alert-dialog :title="tags.alert" :errMsgs="tags.errMsgs" ref="alertDlg"></alert-dialog>
`
}